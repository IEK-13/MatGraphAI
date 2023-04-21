from django_neomodel import DjangoNode, classproperty
from neomodel import AliasProperty, StringProperty, UniqueIdProperty, ArrayProperty
from django.apps import apps


class UIDDjangoNode(DjangoNode):
    """
    Abstract base class for nodes with unique IDs in a Django-Neo4j graph.

    python

    uid: A unique identifier property, serving as the primary key.
    """

    uid = UniqueIdProperty(primary_key=True)
    __abstract_node__ = True

    @classproperty
    def _meta(cls):
        """
        A class property that retrieves metadata for the model, including
        app_label, concrete_model, and an AliasProperty for the primary key.

        app_label: The Django app label associated with this model.
        concrete_model: The concrete model associated with the metadata.
        pk: An AliasProperty for the primary key (uid).
        """
        cls.Meta.app_label = apps.get_containing_app_config(cls.__module__).label
        opts = super()._meta
        opts.concrete_model = opts.model
        cls.pk = AliasProperty(to='uid')
        return opts

    class Meta:
        """
        A class for defining metadata options for the UIDDjangoNode model.
        """
        pass

    def __hash__(self):
        """
        Computes the hash value of the UIDDjangoNode instance based on its unique identifier (uid).

        Raises a TypeError if the uid is not set.
        """
        if self.uid is None:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self.uid)


class UniqueNode(DjangoNode):
    """
    Abstract base class for unique nodes in a Django-Neo4j graph.

    uid: A unique identifier property.
    """
    uid = UniqueIdProperty()
    __abstract_node__ = True

    @classmethod
    def category(cls):
        pass


class CausalObject(UIDDjangoNode):
    """
    Abstract base class representing causal objects in the knowledge graph.

    name: The name of the causal object.
    date_added: The date the causal object was added to the knowledge graph.
    """
    name = StringProperty()
    __abstract_node__ = True

    date_added = StringProperty(required=True)

    def __str__(self):
        return self.name


class OntologyNode(UIDDjangoNode):
    """
    Abstract base class representing ontology nodes in the knowledge graph.

    EMMO__name: The name of the ontology node according to the EMMO.
    EMMO__uri: The unique URI of the ontology node according to the EMMO.
    """
    EMMO__name = StringProperty(required=True, unique_index=True)
    EMMO__uri = StringProperty(required=True, unique_index=True)
    __abstract_node__ = True

    def __str__(self):
        return self.EMMO__name


class AlternativeLabelMixin:
    """
    Mixin class for nodes with alternative labels.

    alternative_labels: An array of alternative labels for the node.
    """
    alternative_labels = ArrayProperty(
        StringProperty(),
        required=False,
        index=True
    )
