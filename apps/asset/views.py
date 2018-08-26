from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from apps.repository import models
from ..salt.core import SaltApiClient
from . import forms


# from deployment.models import project
# Create your views here.


def raise_exception(request):
    return HttpResponse('<h2>错误<h2>')

@login_required
def home(request):
    return HttpResponseRedirect('/index')

@login_required
def index(request):
    # host_count = models.hostinfo.objects.count()
    host_count = 10
    # vps_count = models.vpsinfo.objects.count()
    vps_count = 10
    user_count = models.UserProfile.objects.count()
    # project_count = models.project.objects.count()
    project_count = 10
    return  render(request, 'asset/index.html', {
        'host_count':host_count,
        'user_count':user_count,
        'vps_count':vps_count,
        'project_count':project_count,
    })


def login(request):
    if request.method == 'GET':
        form = forms.LoginAuthForm()
        return render(request, 'asset/login.html', {'form': form})
    else:
        form = forms.LoginAuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/index')
            else:
                return render(request, 'asset/login.html', {'form':form, 'password_is_wrong':True})
        else:
            return render(request, 'asset/login.html', {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')

@login_required
def changepassword(request):
    if request.method == 'GET':
        form = forms.ChangePasswdForm()
        return render(request, 'asset/changepassword.html', {'form':form})
    else:
        form = forms.ChangePasswdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('new_password')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 == new_password2:
                user = auth.authenticate(username=username,password=old_password)
                if user is not None and user.is_active:
                    new_password = form.cleaned_data.get('new_password')
                    user.set_password(new_password)
                    user.save()
                    User = auth.authenticate(username=username,password=new_password)
                    auth.login(request,User)
                    return HttpResponseRedirect('/index')
                else:
                    return render(request, 'asset/changepassword.html', {'form':form, 'old_password_wrong':True})
            else:
                return render(request, 'asset/changepassword.html', {'form':form, 'new_password_wrong':True})
        else:
            return render(request, 'asset/changepassword.html', {'form':form})

# @login_required
# def host_all(request,comm):
#     if comm == 'list':
#         hosts = models.hostinfo.objects.all()
#         return render(request, 'asset/hostlist.html', {'hosts': hosts})
#     if comm == 'add':
#         if request.method == 'POST':
#             form = forms.AddHostForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 tips = '添加成功'
#                 form = forms.AddHostForm()
#                 return render(request, 'asset/add.html', {'form': form, 'tips': tips, 'title': '添加主机'})
#         else:
#             form = forms.AddHostForm()
#             return render(request, 'asset/add.html', {'form': form, 'title': '添加主机'})
#     if comm == 'edit':
#         hostid = request.GET.get('hostid')
#         host_obj = models.hostinfo.objects.get(id=hostid)
#         if request.method == 'POST':
#             form = forms.AddHostForm(request.POST,instance=host_obj)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('/host/list/')
#         else:
#             form = forms.AddHostForm(instance=host_obj)
#             return render(request, 'asset/add.html', {'form':form, 'title': '修改主机信息'})
#     if comm == 'delete':
#         hostid = request.GET.get('hostid')
#         host_obj = models.hostinfo.objects.get(id=hostid)
#         host_obj.delete()
#         return HttpResponseRedirect('/host/list')
#
# @login_required
# def vps_all(request,comm):
#     if comm == 'list':
#         vpss = models.vpsinfo.objects.all()
#         return render(request, 'asset/vpslist.html', {'vpss': vpss})
#     if comm == 'add':
#         if request.method == 'POST':
#             form = forms.AddVpsForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 tips = '添加成功'
#                 form = forms.AddHostForm()
#                 return render(request, 'asset/add.html', {'form': form, 'tips': tips, 'title': '添加VPS'})
#         else:
#             form = forms.AddHostForm()
#             return render(request, 'asset/add.html', {'form': form, 'title': '添加VPS'})
#     if comm == 'edit':
#         vpsid = request.GET.get('vpsid')
#         vps_obj = models.vpsinfo.objects.get(id=vpsid)
#         if request.method == 'POST':
#             form = forms.AddVpsForm(request.POST,instance=vps_obj)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('/vps/list/')
#         else:
#             form = forms.AddVpsForm(instance=vps_obj)
#             return render(request, 'asset/add.html', {'form':form, 'title': '修改VPS信息'})
#     if comm == 'delete':
#         vpsid = request.GET.get('vpsid')
#         vps_obj = models.vpsinfo.objects.get(id=vpsid)
#         vps_obj.delete()
#         return HttpResponseRedirect('/vps/list')
#
# @login_required
# def user_all(request,comm):
#     if comm == 'list':
#         users = User.objects.all()
#         return render(request, 'asset/userlist.html', {'users': users})
#     if comm == 'add':
#         if request.method == 'POST':
#             form = forms.AddUser(request.POST)
#             if form.is_valid():
#                 form.save()
#                 tips = '添加成功'
#                 form = forms.AddUser()
#                 return render(request, 'asset/add.html', {'form': form, 'tips': tips, 'title': '添加用户'})
#         else:
#             form = forms.AddUser()
#             return render(request, 'asset/add.html', {'form': form, 'title': '添加用户'})
#     if comm == 'edit':
#         userid = request.GET.get('userid')
#         user_obj = User.objects.get(id=userid)
#         if request.method == 'POST':
#             form = forms.AddUser(request.POST,instance=user_obj)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('/user/list/')
#         else:
#             form = forms.AddUser(instance=user_obj)
#             return render(request, 'asset/add.html', {'form':form, 'title': '修改用户信息'})
#     if comm == 'delete':
#         userid = request.GET.get('userid')
#         user_obj = models.vpsinfo.objects.get(id=userid)
#         user_obj.delete()
#         return HttpResponseRedirect('/user/list')
#
# @login_required
# def usergroup_all(request,comm):
#     if comm == 'list':
#         groups = Group.objects.all()
#         return render(request, 'asset/usergrouplist.html', {'groups': groups})
#     if comm == 'add':
#         if request.method == 'POST':
#             form = forms.AddUserGroup(request.POST)
#             if form.is_valid():
#                 form.save()
#                 tips = '添加成功'
#                 form = forms.AddUserGroup()
#                 return render(request, 'asset/add.html', {'form': form, 'tips': tips, 'title': '添加团队'})
#         else:
#             form = forms.AddUserGroup()
#             return render(request, 'asset/add.html', {'form': form, 'title': '添加团队'})
#     if comm == 'edit':
#         groupid = request.GET.get('groupid')
#         group_obj = Group.objects.get(id=groupid)
#         if request.method == 'POST':
#             form = forms.AddUserGroup(request.POST,instance=group_obj)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('/usergroup/list/')
#         else:
#             form = forms.AddUserGroup(instance=group_obj)
#             return render(request, 'asset/add.html', {'form':form, 'title': '修改团队信息'})
#     if comm == 'delete':
#         groupid = request.GET.get('groupid')
#         group_obj = Group.objects.get(id=groupid)
#         group_obj.delete()
#         return HttpResponseRedirect('/usergroup/list/')
#
#
# def hostgroup(request):
#     return HttpResponse('<h1>功能正在开发中。。。</h1>')
#
# def equipment(request):
#     return HttpResponse('<h1>功能正在开发中。。。</h1>')
#
# def hostremoteuser(request):
#     return HttpResponse('<h1>功能正在开发中。。。</h1>')
