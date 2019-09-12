from django.db import models
#from people.models import Colaborador
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField


class Tag(models.Model):
	name = models.CharField(max_length=31, unique=True )
	slug = models.SlugField(max_length=31, unique = True, help_text = 'Una etiqueta para configuracion de la url.')

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('question_ask_create')

	def getCantidadPreguntasEtiquetadas(self):
		return Pregunta.objects.filter(tag=self).count()

	def get_questionsTag(self):
		return reverse('question_detail_ByTag', kwargs={'id': self.id})


	
class Pregunta(models.Model):
	titulo = models.CharField(max_length=100, unique=True)
	img_issue = models.ImageField('Cargar imagen',upload_to = 'img_preguntas', blank=True, null=True)
	descripcion = HTMLField()#models.TextField(max_length=700, blank=True)
	#codigo = models.TextField(max_length=700, blank=True)
	
	#slug = models.SlugField(max_length=31, unique = True, blank=True)
	colaboradores = models.ForeignKey('people.Colaborador')
	fecha = models.DateField('fecha de publicación', auto_now_add=True)
	tag = models.ForeignKey(Tag)

	def __str__(self):
		return self.titulo.title()

	def get_absolute_url(self):
		return reverse('question_detail_fromindex', kwargs={'id': self.id})

	def getCantidadeRespuesta(self):
		return Respuesta.objects.filter(pregunta=self).count()

	def getNombreEtiqueta(self):
		return tag.objects.filter(id=self.tag)

	def admin_foto(self):
		#return '<img src="media/%s" width="100" height="100" alt="Foto de estudiante"/>' % (self.foto) este no es el real
		#return mark_safe('<img src="%s" width="120" height="100" alt="Sin foto"/>' % (self.foto.url)) REAL
		if self.img_issue:
			return mark_safe('<a href="{0}"><img src="{0}"  alt="Not image" width="400px" height="400px"></a>'.format(self.img_issue.url))

	def get_update_url(self):
		return reverse('question_update', kwargs={'pk': self.pk})

	def get_delete_url(self):
		return reverse('question_delete', kwargs={'pk': self.pk})
		
  
	#def get_question_withoutR_url(self):
		#return reverse('question_list_withouR')
	



class Respuesta(models.Model):
	descripcion_img = models.ImageField('Cargar imagen',upload_to = 'img_respuestas', blank=True,  null=True)
	#descripcion_code = models.TextField('Mostrar código', max_length=700, )
	descripcion = HTMLField()#models.TextField( 'Descripción', max_length=700)
	pregunta = models.ForeignKey(Pregunta)
	Colaborador = models.ForeignKey('people.Colaborador', related_name='colaboradores')
	fecha = models.DateField('fecha de publicación', auto_now_add=True)

	def __str__(self):
		return self.descripcion.title()

	def get_absolute_url(self):
		return reverse('question_detail_fromindex', kwargs={'id': self.pregunta.id})

	def admin_foto(self):
		#return '<img src="media/%s" width="100" height="100" alt="Foto de estudiante"/>' % (self.foto) este no es el real
		#return mark_safe('<img src="%s" width="120" height="100" alt="Sin foto"/>' % (self.foto.url)) REAL
		if self.descripcion_img:
			return mark_safe('<a href="{0}"><img src="{0}"  alt="Not image" width="300px" height="300px"></a>'.format(self.descripcion_img.url))

	def get_update_url(self):
		return reverse('answer_update', kwargs={'pk': self.pk})

	def get_delete_url(self):
		return reverse('answer_delete', kwargs={'pk': self.pk})

	
		






