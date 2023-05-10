from django_neomodel import DjangoNode, classproperty
from neomodel import AliasProperty, StringProperty, UniqueIdProperty, ArrayProperty, RelationshipTo, ZeroOrMore
from django.apps import apps


class UIDDjangoNode(DjangoNode):
    uid = UniqueIdProperty(
        primary_key=True
    )

    __abstract_node__ = True

    # django (esp. admin) uses .pk in a few places and expects a UUID.
    # add an AliasProperty to handle this
    @classproperty
    def _meta(self):
        self.Meta.app_label = apps.get_containing_app_config(self.__module__).label
        opts = super()._meta
        self.pk = AliasProperty(to='uid')
        return opts

    class Meta:
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

    name: The name of the ontology node according to the EMMO.
    uri: The unique URI of the ontology node according to the EMMO.
    """
    name = StringProperty()
    uri = StringProperty()
    description = StringProperty()
    alternative_label =RelationshipTo('graphutils.models.AlternativeLabel', 'HAS_LABEL', cardinality=ZeroOrMore)
    __abstract_node__ = True

    def __str__(self):
        return self.name


