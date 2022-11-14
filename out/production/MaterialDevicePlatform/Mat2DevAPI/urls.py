from django.urls import path
from django.urls import re_path as url

from . import views
from Mat2DevAPI.views.matterView import ElementAutocompleteView

urlpatterns = [
    url(
        r'^autocomplete/element/$',
        ElementAutocompleteView.as_view(),
        name='element-autocomplete',
    )
]
