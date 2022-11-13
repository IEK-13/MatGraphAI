from x28_ontology.models import Occupation as x28Occupation, SCODirectory
from skills import OntologyOccupation as GraphOccupation, JobCluster

missing_clusters = []
excess_occupations = []
missing_occupations = []

# find missing clusters
for cluster in SCODirectory.objects.get(name="x28 AG").scos.all():
    try:
        JobCluster.nodes.get(ontology_id=cluster.code)
    except JobCluster.DoesNotExist:
        missing_clusters.append(cluster)

# create missing clusters
for cluster in missing_clusters:
    print(f'creating missing cluster: {cluster.name} / {cluster.code}')
    JobCluster(
        label=cluster.name,
        ontology_id=cluster.code
    ).save()


# find missing occupations
for occ in x28Occupation.objects.all():
    try:
        GraphOccupation.nodes.get(ontology_id=occ.id)
    except GraphOccupation.DoesNotExist:
        missing_occupations.append(occ)


# update cluster-occupation relations / find excess occupations in graph
for occ in GraphOccupation.nodes.all():
    try:
        x28occ = x28Occupation.objects.get(id=occ.ontology_id)

        occ.clusters.disconnect_all()
        for cluster in x28occ.scos.filter(sco_directory__name="x28 AG"):
            occ.clusters.connect(
                JobCluster.nodes.get(ontology_id=cluster.code)
            )

    except x28Occupation.DoesNotExist:
        excess_occupations.append(occ)


for occ in missing_occupations:
    print(f'Occupation not found: '+occ.name)

for occ in excess_occupations:
    print(f'Occupation no longer in ontology: '+occ.label)