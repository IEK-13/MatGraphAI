from django.urls import path
from django.urls import re_path as url

from . import views
from Mat2DevAPI.views.matterView import ElementAutocompleteView, MaterialInputAutocompleteView

urlpatterns = [
    url(
        r'^autocomplete/element/$',
        ElementAutocompleteView.as_view(),
        name='element-autocomplete',
    ),
    url(
        r'^autocomplete/manufacturing/$',
        MaterialInputAutocompleteView.as_view(),
        name='material-input-autocomplete',
    ),
]
