from django_neomodel import DjangoNode
from neomodel import AliasProperty, StringProperty, UniqueIdProperty, ArrayProperty
from django.apps import apps


class UIDDjangoNode(DjangoNode):
    """
    Abstract base class for nodes with unique IDs in a Django-Neo4j graph.
    """
    uid = UniqueIdProperty(primary_key=True)
    __abstract_node__ = True

    # Django (esp. admin) uses .pk in a few places and expects a UUID.
    # Add an AliasProperty to handle this
    @classmethod
    def _meta(cls):
        cls.Meta.app_label = apps.get_containing_app_config(cls.__module__).label
        opts = super()._meta
        opts.concrete_model = opts.model
        cls.pk = AliasProperty(to='uid')
        return opts

    class Meta:
        pass

    def __hash__(self):
        if self.uid is None:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self.uid)


class UniqueNode(DjangoNode):
    """
    Abstract base class for unique nodes in a Django-Neo4j graph.
    """
    uid = UniqueIdProperty()
    __abstract_node__ = True

    @classmethod
    def category(cls):
        pass


class CausalObject(UIDDjangoNode):
    """
    Abstract base class representing causal objects in the knowledge graph.
    """
    name = StringProperty()
    __abstract_node__ = True

    date_added = StringProperty(required=True)

    def __str__(self):
        return self.name


class OntologyNode(UIDDjangoNode):
    """
    Abstract base class representing ontology nodes in the knowledge graph.
    """
    EMMO__name = StringProperty(required=True, unique_index=True)
    EMMO__uri = StringProperty(required=True, unique_index=True)
    __abstract_node__ = True

    def __str__(self):
        return self.EMMO__name


class AlternativeLabelMixin:
    """
    Mixin class for nodes with alternative labels.
    """
    alternative_labels = ArrayProperty(
        StringProperty(),
        required=False,
        index=True
    )
