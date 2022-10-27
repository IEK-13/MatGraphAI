from django_neomodel import DjangoNode, classproperty
from neomodel import (AliasProperty,
                      StringProperty,
                      UniqueIdProperty,
                      DateTimeProperty,
                      ArrayProperty)


class UniqueNamedNode(DjangoNode):
    class Meta:
        app_label = 'Mat2DevAPI'

    uid = UniqueIdProperty(
        primary_key=True
    )
    name = StringProperty()
    __abstract_node__ = True

    # django (esp. admin) use .pk in a few places and expect a UUID.
    # add an AliasProperty to handle this
    @classproperty
    def _meta(self):
        opts = super()._meta
        self.pk = AliasProperty(to='uid')
        return opts


class UIDDjangoNode(DjangoNode):
    uid = UniqueIdProperty(
        primary_key=True
    )

    __abstract_node__ = True

    # django (esp. admin) use .pk in a few places and expect a UUID.
    # add an AliasProperty to handle this
    @classproperty
    def _meta(self):
        opts = super()._meta
        self.pk = AliasProperty(to='uid')
        return opts

    class Meta:
        app_label = "Mat2DevAPI"  # required for some django function (esp. admin)


class testClass(UIDDjangoNode):
    def __str__(self):
        return self.uid

    pass


class NamedNode(DjangoNode):
    @classmethod
    def category(cls):
        pass

    date_added = DateTimeProperty(required=True)
    name = StringProperty()
    __abstract_node__ = True


class UniqueNode(DjangoNode):
    @classmethod
    def category(cls):
        pass

    uid = UniqueIdProperty()
    __abstract_node__ = True


class CausalObject(UniqueNamedNode):
    __abstract_node__ = True


class AlternativeLabelMixin:
    alternative_labels = ArrayProperty(
        StringProperty(),
        required=False,
        index=True
    )
