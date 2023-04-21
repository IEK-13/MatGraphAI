from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from .models import CsvFile
from .serializers import CsvFileSerializer

class CsvUploadView(generics.CreateAPIView):
    parser_class = (FileUploadParser,)
    serializer_class = CsvFileSerializer
    queryset = CsvFile.objects.all()
