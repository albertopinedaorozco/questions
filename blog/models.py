from django.db import models
from question.models import Tag
from people.models import Colaborador
from django.core.urlresolvers import reverse
from tinymce.models import HTMLField
from django.utils.safestring import mark_safe

class Post(models.Model):
	title = models.CharField('titulo',max_length = 63)
	pub_date = models.DateField('fecha de publicación', auto_now_add=True)
	slug = models.SlugField('url',max_length=63, help_text = 'Url de la nota', unique_for_month='pub_date')
	text = HTMLField('contenido')#models.TextField('contenido')
	img_post = models.ImageField('imagen adjunta',upload_to = 'img_blog', blank=True, null=True)
	#llaves foraneas
	tags = models.ManyToManyField(Tag)
	colaboradores = models.ForeignKey(Colaborador)

	def __str__(self):
		return "{} on {}".format(self.title, self.pub_date.strftime('%Y-%m-%d'))

	class Meta:
		verbose_name = 'Publicaciones'
		ordering = ['-pub_date', 'title']
		get_latest_by = 'pub_date'

	def get_absolute_url(self):
		return reverse('blog_post_detail',kwargs={'year': self.pub_date.year, 'month': self.pub_date.month, 'slug': self.slug})

	def get_update_url(self):
		return reverse('blog_post_update',kwargs={'year': self.pub_date.year, 'month': self.pub_date.month, 'slug': self.slug})

	def get_delete_url(self):
		return reverse('blog_post_delete', kwargs={'year': self.pub_date.year, 'month': self.pub_date.month, 'slug': self.slug})

	def admin_foto(self):
		#return '<img src="media/%s" width="100" height="100" alt="Foto de estudiante"/>' % (self.foto) este no es el real
		#return mark_safe('<img src="%s" width="120" height="100" alt="Sin foto"/>' % (self.foto.url)) REAL
		if self.img_post:
			return mark_safe('<a href="{0}"><img src="{0}"  alt="Not image" width="400px" height="400px"></a>'.format(self.img_post.url))
