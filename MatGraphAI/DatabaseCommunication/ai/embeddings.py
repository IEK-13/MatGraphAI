from DatabaseCommunication.ai.config import EMBEDDING_MODEL, EMBEDDING_FETCHING_PROCESSES, EMBEDDING_DB_CHUNK_SIZE
from typing import List
from tenacity import retry, stop_after_attempt, wait_random_exponential
import openai
from neomodel import db

from DatabaseCommunication.ai.utils import split_dataframe
from Mat2DevAPI.models.ontology import EMMO_Matter


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def request_embedding(text) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = str(text).replace("\n", " ")

    return openai.Embedding.create(input=[text], engine=EMBEDDING_MODEL)["data"][0]["embedding"]


def get_embeddings_for_model(cmd, Model, fetch_properties, combine_func, fetch_filter='', required_properties=None, resume=True, id_property='uid', unwind_alternative_labels=False):

    import pandas as pd
    from pandarallel import pandarallel

    query = f'''
        MATCH (n:{Model.__label__})  
    '''

    if fetch_filter:
        fetch_filter += ' AND '
    fetch_filter += ' COALESCE(n.disable_embedding, false)=false '

    if resume:
        fetch_filter += 'AND NOT(EXISTS((n)<-[:FOR]-(:ModelEmbedding)))'

    if fetch_filter:
        query += f'WHERE {fetch_filter} '
    query += 'RETURN '+', '.join([f'n.{prop} as {prop}' for prop in fetch_properties])

    rows, meta = db.cypher_query(query)

    if not required_properties:
        required_properties = fetch_properties

    # created a separate embedding for every label
    if unwind_alternative_labels:
        initial_rows = rows
        rows = list()
        for row in initial_rows:
            rows.append(row)
            if alternative_labels := row[fetch_properties.index('alternative_labels')]:
                for label in alternative_labels:
                    row = row.copy()
                    row[fetch_properties.index('label')] = label
                    rows.append(row)

    df = pd.DataFrame(rows, columns=fetch_properties)
    total = len(df.index)

    df = df.dropna(subset=required_properties)
    processable = len(df.index)

    cmd.stdout.write(f'total nodes: {total}')
    cmd.stdout.write(f'processable nodes: {processable}')
    cmd.stdout.write(f'skipping {total-processable} nodes...')

    if processable == 0:
        return

    def combine(item):
        if 'embedding_string' in fetch_properties and item['embedding_string']:
            return item['embedding_string']
        return combine_func(item)

    df["combined"] = df.apply(combine, axis=1)

    pandarallel.initialize(
        nb_workers=EMBEDDING_FETCHING_PROCESSES,
        progress_bar=True,
        use_memory_fs=False # does not work in Docker
    )

    df['embedding'] = df.combined.parallel_apply(request_embedding)

    cmd.stdout.write('')
    cmd.stdout.write(cmd.style.SUCCESS('Successfully obtained all embeddings.'))


    cmd.stdout.write('Splitting data for db ingest...')
    chunks = split_dataframe(df[[id_property, 'embedding']], chunk_size=EMBEDDING_DB_CHUNK_SIZE)

    total = len(chunks)
    current = 1

    if not resume:
        cmd.stdout.write('Deleting all existing embeddings...')
        db.cypher_query(f'''
            MATCH (:{Model.__label__})<-[:FOR]-(emb:ModelEmbedding)
            DETACH DELETE emb
        ''')

    for chunk in chunks:

        cmd.stdout.write(f'Storing chunk {current}/{total}...')
        current += 1

        records = chunk.to_records(index=False)
        db_rows = [ # to python array
            [r[0], r[1]] for r in chunk.to_records(index=False)
        ]

        db.cypher_query(f'''
                    UNWIND $vectors as row
                    MATCH
                        (n:{Model.__label__} {{{id_property}: row[0]}})
                    CREATE
                        (emb:ModelEmbedding {{vector: row[1]}})-[:FOR]->(n)
                ''', {'vectors': db_rows})

    cmd.stdout.write(cmd.style.SUCCESS('Successfully stored embeddings in db'))


def combine_labels(elm):
    labels = [elm['label']]
    if alternative_labels := elm.get('alternative_labels'):
        if alternative_labels.__iter__:
            labels += alternative_labels
    return ', '.join(labels)


def get_embeddings_for_ontology(cmd, resume):
    get_embeddings_for_model(
        cmd,
        EMMO_Matter,
        ('uid', 'label', 'alternative_labels'),
        lambda s: 'Studiengang '+s['label'],
        unwind_alternative_labels=True,
        required_properties=('uid', 'label'),
        resume=resume
    )