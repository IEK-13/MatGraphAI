from django.db import models
from neomodel import (
    StringProperty,
    DateTimeProperty,
    IntegerProperty,
    RelationshipTo,
    RelationshipFrom,
)

from Mat2DevAPI.choices.ChoiceFields import INSTITUTION_TYPE_CHOICEFIELD
from Mat2DevAPI.models.abstractclasses import CausalObject, UniqueNode
from Mat2DevAPI.models.relationships import ByRel, InLocationRel


class PIDA(CausalObject):
    """
    Represents a PIDA.
    """
    class Meta:
        app_label = 'Mat2DevAPI'

    pida = StringProperty(unique_index=True, required=True)
    date_added = StringProperty()
    by = RelationshipTo("Researcher", "BY", model=ByRel)
    has = RelationshipTo("CausalObject", "HAS", model=ByRel)
    tag = StringProperty()


class Country(CausalObject):
    """
    Represents a country.
    """
    abbreviation = StringProperty()


class Institution(CausalObject):
    """
    Represents an institution.
    """
    ROI = StringProperty(unique_index=True, required=True)
    link = StringProperty()
    acronym = StringProperty()
    wikipedia_url = StringProperty()
    type = StringProperty(choices=INSTITUTION_TYPE_CHOICEFIELD)


class Instrument(CausalObject):
    """
    Represents an instrument.
    """
    class Meta:
        app_label = 'Mat2DevAPI'

    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)


class Researcher(CausalObject):
    """
    Represents a researcher.
    """
    country = RelationshipTo(Country, "IN", model=InLocationRel)
    institution = RelationshipTo(Institution, "AFFILIATED_TO", model=InLocationRel)

    # Organizational Data
    ORCID = StringProperty(unique=True)
    email = StringProperty()

    class Meta:
        app_label = 'Mat2DevAPI'

    name = StringProperty(unique_index=True, required=True)
    first_author = RelationshipTo("Publication", "FIRST_AUTHOR", model=ByRel)
    author = RelationshipTo("Publication", "AUTHOR", model=ByRel)
    planned = RelationshipTo("Process", "PLANNED", model=ByRel)
    conducted = RelationshipTo("Process", "CONDUCTED", model=ByRel)


class Publication(UniqueNode):
    """
    Represents a publication.
    """
    class Meta:
        app_label = 'Mat2DevAPI'

    DOI = StringProperty(unique_index=True, required=True)
    first_authors = RelationshipFrom(Researcher, "FIRST_AUTHOR")
    measurements = RelationshipFrom("Measurement", "PUBLISHED_IN")
    institution = StringProperty()
    publishing_date = DateTimeProperty()
    citations = IntegerProperty()


class File(CausalObject):
    """
    Represents a file.
    """
    FILE_FORMAT_CHOICES = {
        "pdf": "PDF",
        "tif": "tif",
        "jpg": "JPG",
    }
    link = StringProperty(unique=True)
    format = StringProperty(choices=FILE_FORMAT_CHOICES)
