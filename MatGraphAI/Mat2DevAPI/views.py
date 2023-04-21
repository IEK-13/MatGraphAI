from django.http import HttpResponse

from django.shortcuts import render
import csv
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from Mat2DevAPI.views.uploadCsvViews import upload_csv, results
def index():
    return HttpResponse("Hello, world. You're at the polls index.")



