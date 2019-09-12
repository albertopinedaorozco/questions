from django import forms
from .models import Tag, Pregunta, Respuesta
from people.models import Colaborador
from django.core.exceptions import ValidationError

class RespuestaForm(forms.ModelForm):
	class Meta:
		model = Respuesta
		fields = ['descripcion_img','descripcion','pregunta',]
		exclude = ('pregunta','Colaborador',)
		
	#def clean_descripcion_code(self):
		#return self.cleaned_data['descripcion_code']

	def clean_descripcion_img(self):
		return self.cleaned_data['descripcion_img']
	def clean_descripcion(self):
		return self.cleaned_data['descripcion']
	def clean_pregunta(self):
		return self.cleaned_data['pregunta']

class PreguntaForm(forms.ModelForm):
	class Meta:
		model = Pregunta
		fields = '__all__'
		exclude = ('colaboradores',)
		

	
