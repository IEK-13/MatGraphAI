from django.urls import path, include
from django.urls import re_path as url

from Mat2DevAPI.views.baseViews import analyze, download, upload, home, select_data
from Mat2DevAPI.views.matterView import ElementAutocompleteView, MaterialInputAutocompleteView, MaterialChoiceField
from Mat2DevAPI.views.retrieveDataViews import download_data, download_data_form, FileRetrieveView
from Mat2DevAPI.views.uploadDataViews import upload_csv, FileUploadView, file_upload_form, upload_success

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
    path('upload/', upload, name='upload_csv'),
    path('results/<str:url>/', upload_csv, name='results'),
    path('PIDA_ddl/<str:PID>/', download_data, name='download_data'),
    path('PIDA/<str:PID>/', download_data_form, name='download_data_form'),
    path('fileupload/', FileUploadView, name='file_upload'),    path('fileupload/form/', file_upload_form, name='file_upload_view'),
    path('fileretrieval/<str:uid>/', FileRetrieveView.as_view(), name='file_retrieve'),
    path('upload_success/', upload_success, name='upload_success'),
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('download/', download, name='download'),
    path('analyze/', analyze, name='analyze'),
    path('select-data', select_data, name='select_data'),
]



