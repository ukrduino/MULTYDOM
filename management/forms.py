from django.forms import ModelForm, TextInput
from management.models import Dollar, PriceIndex



class DollarForm(ModelForm):

    class Meta:
        model = Dollar
        exclude = ['dollar_active', 'dollar_date']
        widgets = {'dollar_to_hrn': TextInput(attrs={'size': '2', 'placeholder': 'Курс', 'maxlength': '6'}),
        }


class PriceIndexForm(ModelForm):

    class Meta:
        model = PriceIndex
        exclude = ['priceIndex_active', 'priceIndex_date']
        widgets = {'priceIndexValue': TextInput(attrs={'size': '2', 'placeholder': 'Раз', 'maxlength': '6'}),
        }


# test