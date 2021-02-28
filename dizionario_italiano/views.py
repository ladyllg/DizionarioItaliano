from django.shortcuts import render
from django.views import generic
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import *
import wikiquote, random
from dizionario_italiano import webscraping_cambridge, webscraping_coniugazione
import json

class HomeDizionarioView(View):
    form_class = SearchForm
    template_name = 'definition.html'
    initial = {'parola': ''}
    
    def get_initial(self):
        super(HomeDizionarioView, self).get_initial()
        self.initial = {"parola": parola}
        return self.initial
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()

        quote = random.choice(wikiquote.quotes('Proverbi_italiani',lang='it'))
        return render(request, self.template_name, {'form': form, 'quote': quote} )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            parola = form.cleaned_data['parola']

            response_cambridge = webscraping_cambridge.get_result_cambridge(parola)
            response_coniugazione = webscraping_coniugazione.get_result_coniugazione(parola)
            return render(request, self.template_name, {'form': form, 'parola': parola,
                                                        'response_cambridge': response_cambridge,
                                                        'response_coniugazione': response_coniugazione })


        return render(request, self.template_name, {'form': form})