from django.urls import path, include
from django.urls import re_path as url

from Mat2DevAPI.views.matterView import ElementAutocompleteView, MaterialInputAutocompleteView, MaterialChoiceField
from Mat2DevAPI.views.uploadCsvViews import upload_csv

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
    url(
        r'^autocomplete/ontology/$',
        MaterialChoiceField,
        name='emmomatter-autocomplete'
    ),
    path('upload/', upload_csv, name='upload_csv'),
    path('results/<str:url>/', upload_csv, name='results'),
    path('tagged_data/<str:tag_name>/', views.tagged_data, name='tagged_data'),
    ]



