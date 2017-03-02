from django.shortcuts import render, redirect, HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
import re
import datetime
import bcrypt
DATE_REGEX =  re.compile(r'^(19|20)\d\d[\-\/.](0[1-9]|1[012])[\-\/.](0[1-9]|[12][0-9]|3[01])$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    return render(request, 'main/index.html')

def login(request):
	login = User.objects.login(request.POST)
	if login[0]:
		request.session['user_id']=login[1].id
		return redirect('/friends')
	else:
		messages.warning(request,'User does not exsist')
		return redirect('/')
	return redirect('/friends')

def logout(request):
	request.session.clear()
	return redirect('/')   

def profile(request,id):
	context = {
		'user':User.objects.get(id=id),
	}
	return render(request,"main/profile.html",context)

def friends(request):
	ids=[]
	friends = Friend.objects.filter(userfriend = request.session['user_id'])
	for friend in friends:
		ids.append(friend.newfriend.id)
		ids.append(request.session['user_id'])

	context = {
		'friends': Friend.objects.filter(userfriend=request.session['user_id']),
		'allfriends':User.objects.exclude(id__in=ids),
		'curr_user':User.objects.get(id=request.session['user_id']),
		'users':User.objects.all().exclude(id=request.session['user_id'])
	}
	return render(request, 'main/friends.html',context)

def add_friend(request, id):
	Friend.objects.create(newfriend = User.objects.get(id = id), userfriend= User.objects.get(id=request.session['user_id']))
	return redirect('/friends')
	
def remove_friend(request,id):
	Friend.objects.filter(newfriend__id = id).delete()
	return redirect('/friends')


def register(request):
	if len(request.POST.get('firstname'))<3:
		messages.warning(request,"First Name is not valid")
		return redirect('/')
	elif len(request.POST.get('lastname'))<3:
		messages.warning(request,"Last Name is invalid")
		return redirect('/')
	elif len(request.POST.get('alias'))<3:
		messages.warning(request,"Alias is invalid")
		return redirect('/')	
	elif len(request.POST.get('email'))<3:
		messages.warning(request,"Email is invalid")	
		return redirect('/')	
	elif len(request.POST.get('password'))<6:
		messages.warning(request, "Password must be atleast 6 charachters in length")
		return redirect('/')
	elif request.POST.get('password') != request.POST.get('confirm'):
		messages.warning(request,"Passwords do not match")
		return redirect('/')
	else:
		user = User.objects.create(firstname=request.POST.get('firstname'),lastname=request.POST.get('lastname'),alias=request.POST.get('alias'),birthday=request.POST.get('dob'),email=request.POST.get('email'),password=bcrypt.hashpw(request.POST.get('password').encode(),bcrypt.gensalt())),
		request.session['user_id']=user[0].id
		messages.warning(request,"Please proceed to Login!")
	return redirect('/') 





