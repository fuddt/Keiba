from django import forms


class TicketTypeForm(forms.Form):
    items = [
        ('exacta','馬単'),
        ('quinella','馬連'),
        ('quinella_place','ワイド'),
        ('trio','３連複'),
        ('trifecta','３連単'),
    ]
    ticket_type = forms.ChoiceField(label = '馬券種',choices=items, 
                                   required=True)

class Items(object):
    # make choices horse number 1~18
    num = list(range(1,19))
    items = [(i,'') for i,j in zip(num,num)]
    
class FirstHorseNumberForm(forms.Form):
    first_horse_num = forms.MultipleChoiceField(label='1頭目',choices=Items.items,
                                  widget=forms.CheckboxSelectMultiple(),
                                  help_text='１つは選択をしてください。',
                                  required=True)
    
class SecondHorseNumberForm(forms.Form):
    second_horse_num = forms.MultipleChoiceField(label='2頭目',choices=Items.items,
                                  widget=forms.CheckboxSelectMultiple(),
                                  help_text='1つは選択をしてください。',
                                  required=True)
    
class ThirdHorseNumberForm(forms.Form):
    third_horse_num = forms.MultipleChoiceField(label='3頭目',choices=Items.items,
                                  widget=forms.CheckboxSelectMultiple(),
                                  help_text='1つは選択をしてください。',
                                  required=True)