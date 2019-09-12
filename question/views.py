from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Pregunta, Tag, Respuesta
from people.models import Colaborador
from blog.models import Post
from .forms import RespuestaForm,PreguntaForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User

from django.db.models import Count

def probar(request):
	ques = Pregunta.objects.all().order_by('-id')[:5] #ordenar de forma descendente y top 5
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all()
	return render(request,'question/index.html', {'questions_recents': ques, 'colaboradores_top': colab , 'tag_list': tags,})

def questionlist(request):
	ques = Pregunta.objects.all().order_by('fecha')
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]
	
	return render(request,'question/question_list.html', {'questions_all': ques, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })

def questionlist_byTag(request, id):
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]
	
	quest = Pregunta.objects.all().filter(tag=id)
	nombreTag = Tag.objects.get(id=id).name
	return render(request,'question/question_list_ByTag.html', {'nombreTag': nombreTag,'questions_byTag': quest, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})

def questionlist_WithoutResponses(request):
	quest_withoutR = Pregunta.objects.filter(respuesta__pregunta__isnull=True)
	num_quest_withoutR = Pregunta.objects.filter(respuesta__pregunta__isnull=True).count()
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]
	return render(request,'question/question_without_responses.html', {'questions_withoutR': quest_withoutR, 'num_quest_withoutR': num_quest_withoutR, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })



class QuestionCreate(View): #para registrar la pregunta
	def get(self, request):
		ques = Pregunta.objects.all().order_by('-id')[:5]
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]

		pre = request.GET.get('pregunta')
		#return HttpResponse(pre)
		pregu = Pregunta(titulo=pre)
		preForm = PreguntaForm(instance=pregu)#fields['titulo'].initial = pre
		return render(request,'question/question_form.html', {'form': preForm, 'pregunta': pre, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})

	def post(self, request):
		usu = request.user
		colaborator = Colaborador.objects.get(user=usu)
		ques = Pregunta.objects.all().order_by('-id')[:5]
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]

		bound_form = PreguntaForm(request.POST, request.FILES)

		if bound_form.is_valid():
			new_object = bound_form.save(commit=False)
			new_object.colaboradores = colaborator
			new_object.save()
			return render(request, 'question/index.html', {'questions_recents': ques, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })
		else:
			return render(request,'question/question_form.html',{'form': bound_form, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})
		

class QuestionUpdate(View):
	form_class = PreguntaForm
	model = Pregunta
	template_name = 'question/question_form_update.html'

	def get(self, request, pk):
		pregunt_form = get_object_or_404(Pregunta, pk = pk)
		context = {'form': self.form_class(instance=pregunt_form),'pregunt_form': pregunt_form,}
		return render(request, self.template_name, context)
	
	def post(self, request, pk):
		pregunt_form = get_object_or_404(Pregunta, pk = pk)
		bound_form = self.form_class(request.POST,request.FILES, instance=pregunt_form)

		if bound_form.is_valid():
			new_pregunt_form = bound_form.save()
			return redirect(new_pregunt_form)
		else:
			context = {'form': bound_form, 'pregunt_form': pregunt_form,}
			return render(request, self.template_name, context)

class AnswerUpdate(View):
	form_class = RespuestaForm
	model = Respuesta
	template_name = 'question/answer_form_update.html'

	

	def get(self, request, pk):
		ques = Pregunta.objects.all().order_by('-id')[:5]
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]

		respuest_form = get_object_or_404(Respuesta, pk = pk)
		context = {'form': self.form_class(instance=respuest_form),'respuest_form': respuest_form, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,}
		return render(request, self.template_name, context)
	
	def post(self, request, pk):
		respuest_form = get_object_or_404(Respuesta, pk = pk)
		bound_form = self.form_class(request.POST,request.FILES, instance=respuest_form)

		if bound_form.is_valid():
			new_respuest_form = bound_form.save()
			preguntaObj = Respuesta.objects.get(pk=pk).pregunta#get_object_or_404(Pregunta, pk = pk)
			return redirect(preguntaObj)
		else:
			context = {'form': bound_form, 'respuest_form': respuest_form,}
			return render(request, self.template_name, context)


class QuestionDelete(View):
	form_class = PreguntaForm
	model = Pregunta
	template_name = 'question/question_confirm_delete.html'

	def get(self, request, pk):
		preguntObj = get_object_or_404(Pregunta, pk = pk)
		context = {'pregunta': preguntObj,}
		return render(request, self.template_name, context)
	
	def post(self, request, pk):
		preguntObj = get_object_or_404(Pregunta, pk = pk)
		preguntObj.delete()
		ques = Pregunta.objects.all().order_by('-id')[:5]
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]
		return render(request, 'question/index.html', {'questions_recents': ques, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })

#esta clase es para eliminar respuesta, hay que revisarla toda copy and paste was it
class AnswerDelete(View):
	form_class = RespuestaForm
	model = Respuesta
	template_name = 'question/answer_confirm_delete.html'

	def get(self, request, pk):
		respuestObj = get_object_or_404(Respuesta, pk = pk)
		context = {'respuesta': respuestObj,}
		return render(request, self.template_name, context)
	
	def post(self, request, pk):
		respuestObj = get_object_or_404(Respuesta, pk = pk)
		preguntaObj = Respuesta.objects.get(pk=pk).pregunta#get_object_or_404(Pregunta, pk = pk)
		respuestObj.delete()
		return redirect(preguntaObj)

		#ques = Pregunta.objects.all().order_by('-id')[:5]
		#colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		#for i in range(len(colab)):
		#	colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		#tags = Tag.objects.all().order_by('name')
		#posts = Post.objects.all().order_by('-id')[:10]
		#return render(request, 'question/index.html', {'questions_recents': ques, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })

class RecentsQuestionList(View): #para consultar el listado de preguntas recientes
	def get(self, request):
		ques = Pregunta.objects.all().order_by('-id')[:5]
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]
		return render(request, 'question/index.html', {'questions_recents': ques, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })

class QuestionDetailFromIndex(View): #para mostrar una pregunta especificada con sus respuestas, y permite añadir una respuesta
	form_class = RespuestaForm
	template_name = 'question/question_detail.html'
	

	def get(self, request, id):
		ques = Pregunta.objects.all().order_by('-id')[:5]
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]

		pregunt = get_object_or_404(Pregunta, pk=id)#Pregunta.objects.get(id=id)
		respu = Respuesta.objects.filter(pregunta = pregunt).order_by('fecha')
		return render(request, self.template_name,{'form':self.form_class, 'pregunta': pregunt, 'respuestas': respu, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })

	def post(self, request, id):
		#if user.is_authenticated:
		usu = request.user
		colaborator = Colaborador.objects.get(user=usu)
		ques = Pregunta.objects.all().order_by('-id')[:5]
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]
		#descr_img = request.POST.get('descripcion_img', '')
		#descr_code = request.POST.get('descripcion_code', '')
		#descr = request.POST.get('descripcion', '')
		#colab = request.POST.get('Colaborador', '')
		#preg = get_object_or_404(Pregunta, pk=id)
			
		bound_form = self.form_class(request.POST, request.FILES)
		#bound_form = RespuestaForm(descripcion_img=descr_img,descripcion_code=descr_code,descripcion=descr,Colaborador=colab,pregunta=preg)
			
		if bound_form.is_valid():
			pregunt = get_object_or_404(Pregunta, pk=id)#Pregunta.objects.get(id=id)
			respu = Respuesta.objects.filter(pregunta = pregunt).order_by('fecha')
			bound_form.pregunta = pregunt
			new_respuesta_object = bound_form.save(commit=False)
			new_respuesta_object.pregunta= pregunt
			new_respuesta_object.Colaborador = colaborator
			new_respuesta_object.save()
			#return redirect(new_object)
				
			return render(request, self.template_name,{'form':self.form_class, 'pregunta': pregunt, 'respuestas': respu, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})
			#ques = Pregunta.objects.all().order_by('-id')[:5]
			#colab = Colaborador.objects.all()
			#tags = Tag.objects.all()
			#return render(request, 'question/index.html', {'questions_recents': ques, 'colaboradores_top': colab , 'tag_list': tags,})
		else:
			return render(request,self.template_name,{'form': bound_form, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})
		#else: #si el usuario no esta autenticado
			#return render(request,self.template_name,{'form': bound_form, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})


		
		

