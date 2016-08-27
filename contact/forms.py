from .models import pathlabinfo,pathlab
from django import forms
from django.forms import ModelForm, ModelChoiceField , CheckboxSelectMultiple,MultipleChoiceField

class PathlabForm(ModelForm):
	Path_Lab_Password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = pathlab
		fields = '__all__'

		#fields = ['doc_name','experience', 'fee']
	def __init__(self, *args, **kwargs):
		super(PathlabForm, self).__init__(*args, **kwargs)
		#self.fields['Address_No2_Sub_Locality']
		#self.fields['Address_No3_Area'].required=False
		#self.fields['Nearby_Pincode'].required=False



class PathlabInfoForm(ModelForm):
    Path_Lab_Id = ModelChoiceField(queryset=pathlab.objects.all(), empty_label=None)
#clinic_day  = forms.CharField(required=True,help_text="Eg: {'monday' : ['10:00-12:00', '07:00-08:00'],'tuesday':'07:00-08:00'} ")
    class Meta:
            model = pathlabinfo
            fields = '__all__'

    def __init__(self, *args, **kwargs):
		super(PathlabInfoForm, self).__init__(*args, **kwargs)
		self.fields['Path_Lab_Id'].empty_label = None


