from django.urls import path, include
from django.urls import re_path as url

from Mat2DevAPI.views.matterView import ElementAutocompleteView, MaterialInputAutocompleteView, MaterialChoiceField
from Mat2DevAPI.views.uploadCsvViews import upload_csv
from Mat2DevAPI.views.retrievePIDA import download_data, download_data_form

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
    path('PIDA_ddl/<str:PID>/', download_data, name='download_data'),
    path('PIDA/<str:PID>/', download_data_form, name='download_data_form'),
]



