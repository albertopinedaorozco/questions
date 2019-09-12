from django.db import models
from question.models import Respuesta
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Colaborador(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	#nombres = models.CharField(max_length=15, db_index=True)
	#apellidos = models.CharField(max_length=20, db_index=True)
	#email = models.EmailField(max_length=30)
	#link_facebook = models.URLField(max_length=100,blank=True)
	#link_twitter = models.URLField(max_length=100,blank=True)
	es_estudiante = models.BooleanField(default=True)
	es_docente = models.BooleanField(default=False)
	#slug = models.SlugField(max_length=31)
	foto = models.ImageField(upload_to='fotoscolaboradores',default = 'fotoscolaboradores/profile.png', null=True, blank=True)

	def __str__(self):
		return self.user.first_name.title()

	def getNumerodeColaboraciones(self):
		return Respuesta.objects.filter(Colaborador = self).count()

	def get_absolute_url(self):
		return reverse('people_detail_colaborador', kwargs={'id': self.id})

	def fotoxs(self):
		#return '<img src="media/%s" width="100" height="100" alt="Foto de estudiante"/>' % (self.foto) este no es el real
		#return mark_safe('<img src="%s" width="120" height="100" alt="Sin foto"/>' % (self.foto.url)) REAL
		if self.foto:
			return mark_safe('<img src="{0}" width="60" height="60" alt="Sin foto">'.format(self.foto.url)) #135X140 #<a href="{0}"><img src="{0}" width="100" height="110" alt="Sin foto"></a>
		else:
			return mark_safe('<img src="profile.png" width="60" height="60" alt="Usuario sin foto"/>')

	def admin_foto(self):
		#return '<img src="media/%s" width="100" height="100" alt="Foto de estudiante"/>' % (self.foto) este no es el real
		#return mark_safe('<img src="%s" width="120" height="100" alt="Sin foto"/>' % (self.foto.url)) REAL
		if self.foto:
			return mark_safe('<img src="{0}" width="100" height="110" alt="Sin foto">'.format(self.foto.url)) #135X140 #<a href="{0}"><img src="{0}" width="100" height="110" alt="Sin foto"></a>
		else:
			return mark_safe('<img src="profile.png" width="120" height="100" alt="Usuario sin foto"/>')

	#@receiver(post_save, sender=User)
	def create_profile(sender, **kwargs):
		user = kwargs["instance"]
		
		if kwargs["created"]:
			user_profile = Colaborador.objects.create(user=user)
			user_profile.save()
		#post_save.connect(create_profile, sender=User)

	post_save.connect(create_profile, sender=User)

	
	#def create_user_profile(sender, instance, created, **kwargs):
		#if created:
			#Colaborador.objects.create(user=instance)

	#@receiver(post_save, sender=User)
	#def save_user_profile(sender, instance, **kwargs):
	    #instance.colaborador.save()