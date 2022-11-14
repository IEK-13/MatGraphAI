from django.db import models
from neomodel import (DateTimeProperty,
                      StringProperty,
                      RelationshipFrom,
                      RelationshipTo,
                      IntegerProperty)

from Mat2DevAPI.models.abstractclasses import CausalObject, UniqueNode
from Mat2DevAPI.models.relationships import byResearcherRel


class Institution(CausalObject):
    pass


class Instrument(CausalObject):
    class Meta:
        app_label = 'Mat2DevAPI'

    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)


class Researcher(CausalObject):
    # Organizational Data
    ORCID = StringProperty(unique=True)
    email = StringProperty()

    class Meta:
        app_label = 'Mat2DevAPI'

    name = StringProperty(unique_index=True, required=True)
    facility = StringProperty(unique_index=True, required=True)
    measurements = RelationshipFrom(models.ForeignKey("Measurement",
                                                      on_delete=models.deletion.CASCADE),
                                    "hasParticipant")
    first_author = RelationshipTo(models.ForeignKey("Publication",
                                                    on_delete=models.deletion.CASCADE),
                                  byResearcherRel)
    author = RelationshipTo(models.ForeignKey("Publication",
                                              on_delete=models.deletion.CASCADE),
                            byResearcherRel)
    planned = RelationshipTo(models.ForeignKey("Process",
                                               on_delete=models.deletion.CASCADE),
                             byResearcherRel)
    conducted = RelationshipTo(models.ForeignKey("Process",
                                                 on_delete=models.deletion.CASCADE),
                               byResearcherRel)


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
    FILE_FORMAT_CHOICES = {"pdf": "PDF",
                           "tif": "tif",
                           "jpg": "JPG"}
    link = StringProperty(unique=True)
    format = StringProperty(choices=FILE_FORMAT_CHOICES)
