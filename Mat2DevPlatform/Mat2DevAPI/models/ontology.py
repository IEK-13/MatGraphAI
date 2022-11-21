from Mat2DevAPI.models.abstractclasses import OntologyNode


class OntologyQuantity(OntologyNode):
    class Meta:
        app_label = 'Mat2DevAPI'

class OntologyMaterial(OntologyNode):
    class Meta:
        app_label = 'Mat2DevAPI'

class OntologyComponent(OntologyNode):
    class Meta:
        app_label = 'Mat2DevAPI'

class OntologyDevice(OntologyNode):
    class Meta:
        app_label = 'Mat2DevAPI'

