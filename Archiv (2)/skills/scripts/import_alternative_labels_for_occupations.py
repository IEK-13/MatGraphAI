from x28_ontology.models import Occupation, OccupationAlternative
from skills import OntologyOccupation
from django.db.models import Q



for occ in OntologyOccupation.nodes.all():

    try:
        occ.alternative_labels = list(
            OccupationAlternative.objects.filter(
                Q(system_language__id="de") | Q(system_language__id="en"),
                occupation__id=occ.ontology_id
            ).exclude(gender="UNISEX").values_list('name', flat=True) # exclude topics
        )
        occ.save()

    except Occupation.DoesNotExist:
        print(f'Occupation not found: {occ.ontology_id}')
