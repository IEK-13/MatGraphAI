from django.db import models
from neomodel import (DateTimeProperty,
                      StringProperty,
                      RelationshipFrom,
                      RelationshipTo,
                      IntegerProperty,
                      ArrayProperty)

from Mat2DevAPI.choices.ChoiceFields import INSTITUTION_TYPE_CHOICEFIELD
from Mat2DevAPI.models.abstractclasses import CausalObject, UniqueNode
from Mat2DevAPI.models.relationships import byResearcherRel, affiliatedToRel, inRel


class Country(CausalObject):
    abbreviation = StringProperty()

class Institution(CausalObject):
    ROI = StringProperty(unique_index= True, required = True)
    link =  StringProperty()
    acronym = StringProperty()
    wikipedia_url =  StringProperty()
    type = StringProperty(choices=INSTITUTION_TYPE_CHOICEFIELD)
    pass


class Instrument(CausalObject):
    class Meta:
        app_label = 'Mat2DevAPI'
    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)


class Researcher(CausalObject):
    country = RelationshipTo(Country, "IN", model=inRel)
    institution = RelationshipTo(Country, "AFFILIATED_TO", model= affiliatedToRel)
    # Organizational Data
    ORCID = StringProperty(unique=True)
    email = StringProperty()

    class Meta:
        app_label = 'Mat2DevAPI'

    name = StringProperty(unique_index=True, required=True)
    first_author = RelationshipTo(models.ForeignKey("Publication", on_delete=models.deletion.CASCADE),
                                  "FIRST_AUTHOR",
                                  model = byResearcherRel)
    author = RelationshipTo(models.ForeignKey("Publication", on_delete=models.deletion.CASCADE),
                            "AUTHOR",
                            model = byResearcherRel)
    planned = RelationshipTo(models.ForeignKey("Process",on_delete=models.deletion.CASCADE),
                             "PLANNED",
                             model = byResearcherRel)
    conducted = RelationshipTo(models.ForeignKey("Process", on_delete=models.deletion.CASCADE),
                               "CONDUCTED",
                               model = byResearcherRel)


class Publication(UniqueNode):
    class Meta:
        app_label = 'Mat2DevAPI'

    DOI = StringProperty(unique_index=True, required=True)
    first_authors = RelationshipFrom(Researcher, "firstAuthor")
    measurements = RelationshipFrom(
        models.ForeignKey("Measurement",
        on_delete=models.deletion.CASCADE), "publishedIn")
    institution = StringProperty()
    publishing_date = DateTimeProperty()
    citations = IntegerProperty()


class File(CausalObject):
    FILE_FORMAT_CHOICES = \
        {"pdf": "PDF",
        "tif": "tif",
        "jpg": "JPG"}
    link = StringProperty(unique=True)
    format = StringProperty(choices=FILE_FORMAT_CHOICES)
