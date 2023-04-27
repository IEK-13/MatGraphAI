from django.shortcuts import render
from Mat2DevAPI.models.metadata import PIDA

def tagged_data(request, tag_name):
    filtered_data = PIDA.objects.filter(tag=tag_name)
    context = {'filtered_data': filtered_data, 'tag_name': tag_name}
    return render(request, 'your_app/tagged_data.html', context)