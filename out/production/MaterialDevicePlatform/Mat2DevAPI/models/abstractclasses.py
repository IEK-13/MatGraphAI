from django_neomodel import DjangoNode, classproperty
from neomodel import (AliasProperty,
                      StringProperty,
                      UniqueIdProperty,
                      DateTimeProperty,
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
        self.pk = AliasProperty(to='uid')
        return opts

    class Meta:
        pass


class UINamedNode(UIDDjangoNode):
    name = StringProperty()


class UniqueNode(DjangoNode):
    @classmethod
    def category(cls):
        pass

    uid = UniqueIdProperty()
    __abstract_node__ = True


class CausalObject(UIDDjangoNode):
    date_added = DateTimeProperty(required=True)


class AlternativeLabelMixin:
    alternative_labels = ArrayProperty(
        StringProperty(),
        required=False,
        index=True
    )
