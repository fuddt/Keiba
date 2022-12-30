from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView 
from .forms import *
from .combination import TicketCombination
import itertools
# Create your views here.

class TicketFilter(object):
    
    
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
    
    def exacta_type_ticket_filtering(self,selected_horses):
        for ind,selected_horse in enumerate(selected_horses):
            filtered_ticket = []
            for combi in self.allpatterns:
                split_num = combi.split('-')
                num = split_num[ind]
                if num in selected_horse:
                    filtered_ticket.append(combi)
            self.allpatterns = filtered_ticket

    def place_type_ticket_filtering(self,selected_horses):
        if len(selected_horses) == 3:
            first,second,third = selected_horses
            selected_combinations = list(itertools.product(first,second,third))
        else:
            first,second = selected_horses
            selected_combinations = list(itertools.product(first,second))
        #選択した馬番から組み合わせ作成。ただし2-2-2など同一馬番などでも作成される。
        
        select_tickets = []
        for select_combi in selected_combinations:
            select_tickets.append([ticket for ticket in map(int,(select_combi))])
        #全通りから存在する組み合わせのみを抽出。
        filtered_ticket = []
        for combi in self.allpatterns:
            split_num = combi.split('-')
            num = set([int(i) for i in split_num])
            for select_ticket in select_tickets:
                if set(select_ticket)== num:
                    filtered_ticket.append(combi)
        self.allpatterns = sorted(set(filtered_ticket), key=filtered_ticket.index)

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
        three_horses = [first,second,third]
        two_horses = [first,second]
        #all output ==> filter number 
        if ticket_type == 'trifecta':
            ticket_filter.exacta_type_ticket_filtering(three_horses)
            
        elif ticket_type == 'trio':
            ticket_filter.place_type_ticket_filtering(three_horses)
            
        elif ticket_type  == 'exacta':
            ticket_filter.exacta_type_ticket_filtering(two_horses)                
            
        else: # quinella / quinella_place
            ticket_filter.place_type_ticket_filtering(two_horses)

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
