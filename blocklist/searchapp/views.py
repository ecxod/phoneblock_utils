""" create a view to handle the form input and use the search function """
import xml.etree.ElementTree as ET

from django.shortcuts import render
from django.http import HttpResponse
from django import forms


# Create your views here.

def search_phone_number(phone_number):
    """ search phone numbers """
    tree = ET.parse('blocklist.xml')
    root = tree.getroot()

    for phone_info in root.findall('.//phone-info'):
        phone = phone_info.get('phone')
        if phone.startswith(phone_number):
            return {
                'phone': phone_info.get('phone'),
                'rating': phone_info.get('rating'),
                'votes': phone_info.get('votes')
            }
    return None

class SearchForm(forms.Form):
    """ class handle the search form """
    phone_number = forms.CharField(label='Enter Phone Number', max_length=100)

def search_view(request):
    """ search view """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            result = search_phone_number(form.cleaned_data['phone_number'])
            return render(request, 'results.html', {'result': result})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})



def home_view():
    """ home view """
    return HttpResponse("Welcome to the Home Page!")
