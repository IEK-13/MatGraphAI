from django_neomodel import DjangoNode, classproperty
from neomodel import (AliasProperty,
                      StringProperty,
                      UniqueIdProperty,
                      DateProperty,
                      ArrayProperty)
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
        opts.concrete_model = opts.model
        self.pk = AliasProperty(to='uid')
        return opts

    class Meta:
        pass

    def __hash__(self):
        if self.uid is None:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self.uid)


class UniqueNode(DjangoNode):
    @classmethod
    def category(cls):
        pass

    uid = UniqueIdProperty()
    __abstract_node__ = True


class CausalObject(UIDDjangoNode):
    name = StringProperty()
    __abstract_node__ = True

    date_added = DateProperty(required=True)

    def __str__(self):
        return self.name


class OntologyNode(UIDDjangoNode):
    EMMO__name = StringProperty(required=True, unique_index=True)
    EMMO__uri = StringProperty(required=True, unique_index=True)

    def __str__(self):
        return self.EMMO__name

    __abstract_node__ = True


class AlternativeLabelMixin:
    alternative_labels = ArrayProperty(
        StringProperty(),
        required=False,
        index=True
    )
