from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView 
from .forms import *
from .combination import TicketCombination
# Create your views here.

class TicketFilter(object):
    rank_of_horse = {1:0, 2:1, 3:2}
    def __init__(self,ticket_type):
        self.allpatterns = self.combination_method(ticket_type,18)
        
    def combination_method(self, ticket_type,horse_num):
        ticket_combination = TicketCombination()
        method = {
            'exacta':ticket_combination.combination_exacta(horse_num),
            'quinella':ticket_combination.combination_quinella(horse_num),
            'quinella_place':ticket_combination.combination_quinella_place(horse_num),
            'trio':ticket_combination.combination_trio(horse_num),
            'trifecta':ticket_combination.combination_trifecta(horse_num),
        }
        return method[ticket_type]
    
    def exacta_type_ticket_filtering(self,horses,rank):
        ind = self.rank_of_horse.get(rank)
        filtered_ticket = []
        for combi in self.allpatterns:
            split_num = combi.split('-')
            num = split_num[ind]
            if num in horses:
                filtered_ticket.append(combi)
        self.allpatterns = filtered_ticket

    def place_type_ticket_filtering(self,horses,rank):
        ind = self.rank_of_horse.get(rank)
        filtered_ticket = []
        for combi in self.allpatterns:
            split_num = combi.split('-')
            num = split_num[ind]
            for horse in horses:
                if horse in num:
                    filtered_ticket.append(combi)
        self.allpatterns = filtered_ticket

class IndexView(TemplateView):
    def __init__(self):
        self.params = {
            'ticket_type_form': TicketTypeForm,
            'first_horse':FirstHorseNumberForm,
            'second_horse':SecondHorseNumberForm,
            'third_horse':ThirdHorseNumberForm,
            'bracketFlag': False,
            'number':list(range(1,19))
        }
        
    def get(self, request):
        return render(request,template_name='combination/index.html',context= self.params)
    
    def post(self, request):
        ticket_type = request.POST['ticket_type']
        first = request.POST.getlist('first_horse_num')
        second = request.POST.getlist('second_horse_num')
        third = request.POST.getlist('third_horse_num')
        ticket_filter = TicketFilter(ticket_type)
        #all output ==> filter number 
        if ticket_type == 'trifecta':
            for horses,order in zip([first,second,third],[1,2,3]):
                ticket_filter.exacta_type_ticket_filtering(horses, order)
        elif ticket_type == 'trio':
            for horses,order in zip([first,second,third],[1,2,3]):
                ticket_filter.place_type_ticket_filtering(horses, order)
        elif ticket_type  == 'exacta':
            for horses,order in zip([first,second],[1,2]):
                ticket_filter.exacta_type_ticket_filtering(horses, order)                
        else:
            for horses,order in zip([first,second],[1,2]):
                ticket_filter.place_type_ticket_filtering(horses, order)

        #result of combination method
        result = ticket_filter.allpatterns
        self.params['sum'] = f'合計:{len(result)}通り'
        self.params['result'] = result
        # keep user selected
        self.params['ticket_type_form'] = TicketTypeForm(request.POST)
        self.params['first_horse'] = FirstHorseNumberForm(request.POST)
        self.params['second_horse'] = SecondHorseNumberForm(request.POST)
        self.params['third_horse'] = ThirdHorseNumberForm(request.POST)
        return render(request, template_name='combination/index.html',context= self.params)
# 
