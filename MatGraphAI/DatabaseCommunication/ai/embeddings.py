import logging
from neomodel import db
import openai
from typing import List
from tenacity import retry, stop_after_attempt, wait_random_exponential

from DatabaseCommunication.ai.config import EMBEDDING_DIMENSIONS, EMBEDDING_MODEL, EMBEDDING_FETCHING_PROCESSES, EMBEDDING_DB_CHUNK_SIZE
from DatabaseCommunication.ai.utils import split_dataframe
from Mat2DevAPI.models.ontology import EMMOMatter, EMMOQuantity, EMMOProcess


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def request_embedding(text: str) -> List[float]:
    """
    Retrieve the embedding of the given text using OpenAI's API.

    This function attempts to generate an embedding for the input text using OpenAI's Embedding API.
    If the request fails, it will retry up to 6 times, with an exponential backoff strategy for waiting
    between retries.

    Args:
        text (str): The input text to get the embedding for.

    Returns:
        List[float]: A list of floating-point numbers representing the embedding.
    """

    # Replace newlines in the input text with spaces, as they can negatively affect performance.
    text = str(text).replace("\n", " ")

    # Call the OpenAI Embedding API to create an embedding for the input text.
    # The API response contains the embedding data in a nested structure.
    embedding_response = openai.Embedding.create(input=[text], engine=EMBEDDING_MODEL)

    # Extract the embedding data from the response and return it as a list of floating-point numbers.
    return embedding_response["data"][0]["embedding"]



# designed to run via admin-command. uses cmd to print logs
def get_embeddings_for_model(cmd, Model, fetch_properties, combine_func, fetch_filter='', required_properties=None, resume=True, id_property='uid', unwind_alternative_labels=False):
    """
    Retrieve and store embeddings for the specified model using OpenAI's API.

    Args:
        cmd: A command object to handle logging and output.
        Model: The model class for which embeddings should be fetched.
        fetch_properties: A list of properties to fetch from the model nodes.
        combine_func: A function to combine fetched properties before sending them for embedding generation.
        fetch_filter (str, optional): A Cypher query filter to apply when fetching nodes. Defaults to ''.
        required_properties (list, optional): A list of properties that must be present for a node to be processed. Defaults to None.
        resume (bool, optional): Whether to resume the process by skipping nodes that already have embeddings. Defaults to True.
        id_property (str, optional): The property to use as the unique identifier for nodes. Defaults to 'uid'.
        unwind_alternative_labels (bool, optional): Whether to create a separate embedding for every label. Defaults to False.
    """
    import pandas as pd
    from pandarallel import pandarallel

    # Build the Cypher query to fetch nodes of the specified model with the given filter.
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
    # Apply the combine_func on each row of the DataFrame
    df["combined"] = df.apply(combine, axis=1)

    # Initialize pandarallel to parallelize the embedding generation process
    pandarallel.initialize(
        nb_workers=EMBEDDING_FETCHING_PROCESSES,
        progress_bar=True,
        use_memory_fs=False # does not work in Docker
    )

    # Apply the request_embedding function on the combined column of the DataFrame
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


def get_embeddings_for_ontology(cmd, resume):
    """
    Get embeddings for EMMOProcess, EMMOMatter, and EMMOQuantity models.

    Args:
        cmd: Command instance to print logs.
        resume (bool): Whether to resume the process or start from scratch.
    """

    # Get embeddings for EMMOProcess
    get_embeddings_for_model(
        cmd,
        EMMOProcess,
        ('uri', 'label', 'alternative_labels'),
        lambda s: 'Studiengang '+s['label'],
        unwind_alternative_labels=True,
        required_properties=('uid', 'label'),
        resume=resume
    )

    # Get embeddings for EMMOMatter
    get_embeddings_for_model(
        cmd,
        EMMOMatter,
        ('uid', 'label', 'alternative_labels'),
        lambda o: o['label'],
        required_properties=('uid', 'label'),
        unwind_alternative_labels=True,
        #('uid', 'label', 'alternative_labels'),
        #combine_labels,
        #required_properties=('uid', 'label'),
        resume=resume
    )

    # Get embeddings for EMMOQuantity
    get_embeddings_for_model(
        cmd,
        EMMOQuantity,
        ('uid', 'label'),
        lambda e: e['label'],
        resume=resume
    )




# loads embeddings for a model into RAM and enables fast search using FAISS
# index is fetched and built on instance creation
class EmbeddingSearch:
    """
    Loads embeddings for a model into RAM and enables fast search using FAISS.
    The index is fetched and built on instance creation.

    Attributes:
        Model: The Django model class to fetch embeddings for.
        id_property (str): The property to use as the identifier.
    """

    def __init__(self, Model, fetch_filter="true", id_property='uid'):
        """
        Initialize the EmbeddingSearch instance.

        Args:
            Model: The Django model class to fetch embeddings for.
            fetch_filter (str): The filter to apply when fetching embeddings from the database.
            id_property (str): The property to use as the identifier.
        """

        # import here to avoid loading faiss for everything django does
        import faiss
        import numpy as np

        self.Model = Model
        self.id_property = id_property

        logging.info(f'Fetching embeddings for label {Model.__label__}')

        # Fetch embeddings from the database
        result, meta = db.cypher_query(f'''
            MATCH (n:{Model.__label__})<-[:FOR]-(emb:ModelEmbedding)
            WHERE COALESCE(n.disable_embedding, false)=false AND {fetch_filter}
            RETURN n.{id_property} as {id_property}, emb.vector as vector
        ''')

        if not len(result):
            raise ValueError(f'no embeddings found for {Model.__label__}')

        logging.info(f'Creating embedding index for label {Model.__label__}')

        # Create FAISS index
        self.index = faiss.IndexFlatIP(EMBEDDING_DIMENSIONS)
        self.index.add(np.array([
            np.array(row[1]) for row in result
        ]))

        self.model_ids = [row[0] for row in result]


    def find_vector(self, vector, n=1, include_similarities=False):
        """
        Find the closest embeddings in the index to the input vector.

        Args:
            vector (np.array): The input vector to find the closest embeddings for.
            n (int): The number of closest embeddings to return.
            include_similarities (bool): Whether to include similarities in the output.

        Returns:
            If `include_similarities` is False, returns a list of ids or a single id (if n=1).
            If `include_similarities` is True, returns a list of tuples (id, similarity) or a tuple (id, similarity) if n=1.
        """

        import numpy as np

        D, I = self.index.search(np.array([vector]), n)
        ids = [self.model_ids[i] for i in I[0]]

        if include_similarities:
            return ids[0], D[0][0] if n == 1 else [(ids[i], D[0][i]) for i in range(len(ids))]

        return ids[0] if n == 1 else ids


    def find_string(self, query, return_model=False, include_similarity=False, **kwargs):
        """
        Find the closest embeddings in the index to the input query.

        Args:
            query (str): The input string to find the closest embeddings for.
            return_model (bool): Whether to return a model instance instead of the id.
            include_similarity (bool): Whether to include similarities in the output.
            **kwargs: Additional keyword arguments to pass to the `find_vector` method.

        Returns:
            Depending on the input arguments, returns:
            - An instance of the model or an id
            - A list of tuples (model instance, similarity) or a list of tuples (id, similarity)
        """

        if not query:
            return (None, 0) if include_similarity else None
        res = self.find_vector(request_embedding(query), include_similarities=include_similarity, **kwargs)

        if include_similarity:
            if return_model:
                return self.Model.nodes.get(**{self.id_property: res[0]}), res[1]
            else:
                return res
        else:
            return self.Model.nodes.get(**{self.id_property: res}) if return_model else res