from dal import autocomplete
from django.shortcuts import render, redirect


class AutocompleteView(autocomplete.Select2QuerySetView):
    model = None

    label_property = 'name'
    value_property = 'uid'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.model.nodes.none()
        return self.model.nodes.filter(**{self.label_property + '__icontains': self.q})

    def get_result_value(self, result):
        return str(getattr(result, self.value_property))

    def get_result_label(self, result):
        return str(getattr(result, self.label_property))



def home(request):
    return render(request, 'home.html')

def upload(request):
    return render(request, 'upload.html')

def download(request):
    return render(request, 'download.html')

def analyze(request):
    return render(request, 'analyze.html')


def select_data(request):
    data_type = request.GET.get('data_type', None)
    if data_type == 'measurement':
        return redirect('measurement_query')
    elif data_type == 'materials':
        # Redirect to materials data page
        pass
    elif data_type == 'simulation':
        # Redirect to simulation data page
        pass
    elif data_type == 'fabrication':
        # Redirect to fabrication data page
        pass
    else:
        # Redirect to an error page or show a message if the selection is not valid
        pass