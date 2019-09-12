from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import View
from .models import Colaborador
from .forms import ColaboradorForm,UserForm,EditProfileForm

from question.models import Pregunta, Respuesta, Tag
from blog.models import Post

from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate

from django.db.models import Count

from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def ColaboradorList(request):
	colaboradores = Colaborador.objects.all()
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]
	
	return render(request,'people/colaborador_list.html', {'colaboradores': colaboradores, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, })


def getColaboradores(request):

	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]

	colabTodos = Colaborador.objects.all()
	return render(request,'people/people_colaboradores_top.html', {'colaboradores': colabTodos, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})

def getColaboradorDetail(request, id):
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]

	colabDetail = get_object_or_404(Colaborador, pk=id)
	return render(request,'people/people_detail_colaborador.html', {'colaborador': colabDetail, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})

class ColaboradorCreate(View):

	def get(self, request):
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]

		user_form = UserForm()

		return render(request,'people/colaborador_form.html', {'form': ColaboradorForm,'user_form': user_form ,'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})

	def post(self, request):
		colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
		for i in range(len(colab)):
			colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
		tags = Tag.objects.all().order_by('name')
		posts = Post.objects.all().order_by('-id')[:10]

		user_form = UserForm(request.POST)
		bound_form = ColaboradorForm(request.POST, request.FILES)

		if bound_form.is_valid() and user_form.is_valid():
			userName = user_form.cleaned_data['username']
			eMail = user_form.cleaned_data['email']
			passWord = user_form.cleaned_data['password1']

			if not (User.objects.filter(username=userName).exists() or User.objects.filter(email=eMail).exists()):
				foto = bound_form.cleaned_data['foto']				
				created_user = user_form.save()
				#bound_form = ColaboradorForm(request.POST, request.FILES)
				new_object = Colaborador.objects.get(user=created_user )
				new_object.foto = foto
				new_object.save()
				return render(request, 'people/people_detail_colaborador.html', {'colaborador': new_object, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})
			else:
				raise forms.ValidationError('El usuario o Email ya existe')
			


			
		else:
			return render(request,'people/colaborador_form.html',{'form': bound_form, 'user_form': UserForm(), 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts,})

def profile(request):
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]

	colaborator = Colaborador.objects.get(user=request.user)

	args= {'user': request.user,'colaborator': colaborator,'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, }
	return render(request, 'people/profile.html',args)

def edit_profile(request):
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]
	colaborator = Colaborador.objects.get(user=request.user)

	if request.method == 'POST':
		

		form = EditProfileForm(request.POST, instance=request.user)
		form_colab_porfoto = ColaboradorForm(request.POST, request.FILES, instance=request.user )

		if form.is_valid() and form_colab_porfoto.is_valid():
			newFoto = form_colab_porfoto.cleaned_data['foto']
			form.save()
			#form_colab_porfoto.save(commit=False)
			#form_colab_porfoto.foto = newFoto
			#form_colab_porfoto.save()
			if newFoto is not None: #it is not working mmmmmm...
				colaborator.foto = newFoto
				colaborator.save()
			args= {'user': request.user, 'colaborator': colaborator, 'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, }
			return render(request, 'people/profile.html',args)
			#return redirect('/profile/')
	else:
		form = EditProfileForm(instance=request.user)
		form_colab_porfoto = ColaboradorForm(request.POST)
		args = {'form': form,'form_colab_porfoto': form_colab_porfoto ,'colaborator': colaborator,'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, }
		return render(request, 'people/edit_profile.html', args)

def change_password(request):
	colaborator = Colaborador.objects.get(user=request.user)
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-id')[:10]
	

	if request.method == 'POST':
		

		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			args= {'user': request.user,'colaborator': colaborator ,'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, }
			update_session_auth_hash(request, form.user)
			return render(request, 'people/profile.html',args)
			#return redirect('/profile/')
		else:
			args= {'form': form,'user': request.user,'colaborator': colaborator ,'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, }
			return render(request, 'people/change_password.html',args)
	else:
		form = PasswordChangeForm(user=request.user)
		args = {'form': form,'colaborator': colaborator ,'colaboradores_top': colab , 'tag_list': tags, 'posts' : posts, }
		return render(request, 'people/change_password.html', args)





