from datetime import date
from django.urls import reverse
from django.core.files.storage import default_storage
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from rest_framework import views, status, parsers
from rest_framework.response import Response
from Mat2DevAPI.models.metadata import File
from Mat2DevAPI.serializers import UploadedFileSerializer
from django.shortcuts import render, redirect
from neomodel import db
import requests
from wsgiref.util import FileWrapper
import re


def upload_success(request):
    return render(request, 'upload_success.html')
def create_file_node(uid, file_name, file_path):
    """
    Create a new node in the database representing a file.

    :param uid: The unique ID of the file.
    :param file_name: The name of the file.
    :param file_path: The path of the file in local storage.
    """
    db.cypher_query("CREATE (f:File {uid: $uid, file_name: $file_name, file_path: $file_path})",
                    {"uid": uid, "file_name": file_name, "file_path": file_path})


def file_upload_form(request):
    """
    A Django view for rendering the file upload form and handling file uploads.

    :param request: The HTTP request object.
    :return: The rendered file upload form or the JSON response after processing a file upload.
    """

    if request.method == 'POST':
        file_upload_view = FileUploadView.as_view()
        response = file_upload_view(request)

        if response.status_code == 201:
            # Redirect the user to the success page
            return HttpResponseRedirect(response.data['redirect_url'])
        else:
            return JsonResponse(response.data, status=response.status_code)

    return render(request, 'file_upload_form.html')




class FileUploadView(views.APIView):
    """
    A Django view that receives a file uploaded by the user, saves it locally,
    and uploads it to a remote server.
    """
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def post(self, request, **kwargs):
        # Retrieve the uploaded file from the request
        file_obj = request.FILES['file']
        file_name = file_obj.name
        # Save the uploaded file to local storage
        file_path = default_storage.save(file_name, file_obj)

        # Construct the remote URL using the file_name
        url = f"http://134.94.199.40/{file_name}"

        # Define payload and headers for the request
        payload = {'user': 'TLxtWQZbhc', 'password': '50PVZNIO5Q'}

        # Reset the file pointer to the beginning of the file
        file_obj.seek(0)

        # Prepare the files dictionary for the request
        files = [
            ('files', (file_name, file_obj.read()))
        ]
        headers = {
            'Accept': '*/*'
        }

        # Make the POST request to the remote server to upload the file
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        today = date.today()
        file_id = response.json()['id']

        # Save the uploaded file information in the database
        uploaded_file = File(name=file_name, date_added=today, path=file_path, uid=file_id)
        uploaded_file.save()
        if response.status_code == 200:
            create_file_node(uploaded_file.id, file_name, file_path)
            serializer = UploadedFileSerializer(uploaded_file)
            return Response({'success': True, 'redirect_url': reverse('upload_success')}, status=status.HTTP_201_CREATED)
        else:
            try:
                json_data = response.json()
            except ValueError:
                json_data = {'error': 'Invalid JSON response from the file server'}

            return Response(json_data, status=response.status_code)


class FileRetrieveView(views.APIView):
    """
    A Django view that retrieves a file from a remote server and serves it
    as a download to the user.
    """
    def get(self, request, uid, *args, **kwargs):
        # Construct the remote URL using the given uid
        url = f"http://134.94.199.40/{uid}"
        # Define payload and headers for the request
        payload = 'user=TLxtWQZbhc&password=50PVZNIO5Q'
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # Make the GET request to the remote server with stream=True to download the file
        response = requests.get(url, headers=headers, data=payload, stream=True)

        # Extract the filename from the Content-Disposition header
        content_disposition = response.headers.get('Content-Disposition')
        match = re.search(r'filename="(.+)"', content_disposition)
        filename = match.group(1) if match else 'download.bin'

        # Create an HttpResponse object with the content and content type from the external response
        django_response = FileResponse(
            FileWrapper(response.raw),
            content_type=response.headers.get('Content-Type')
        )

        # Set the Content-Disposition header to trigger a download with the extracted filename
        django_response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return django_response
