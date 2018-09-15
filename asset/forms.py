from django import forms
from django.contrib.auth.models import Group
from apps.core.models import UserProfile


class LoginAuthForm(forms.Form):
    username = forms.CharField(
        max_length = 50,
        label = '用户名',
        error_messages = {'required':'请输入用户名'},
        widget = forms.TextInput(attrs={'placeholder':'username'})
    )
    password = forms.CharField(
        max_length = 50,
        label = '密码',
        error_messages = {'required':'请输入密码'},
        widget = forms.PasswordInput(attrs={'placeholder':'password'})
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('用户名和密码为必填项')
        else:
            cleaned_data = super(LoginAuthForm, self).clean()
            return cleaned_data


class ChangePasswdForm(forms.Form):
    old_password = forms.CharField(
        max_length = 50,
        label = '原密码',
        error_messages = {'required':'请输入原密码'},
        widget = forms.PasswordInput(attrs = {'placeholder':'old password'})
    )

    new_password = forms.CharField(
        max_length=50,
        label = '新密码',
        error_messages={'required':'请输入新密码'},
        widget=forms.PasswordInput(attrs={'placeholder':'new password'})
    )

    new_password2 = forms.CharField(
        max_length=50,
        label='确认密码',
        error_messages={'required':'请再次输入新密码'},
        widget=forms.PasswordInput(attrs={'placeholder':'new password'})
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('所有项为必填项')
        else:
            cleaned_data = super(ChangePasswdForm, self).clean()
            return cleaned_data

# class AddVpsForm(forms.ModelForm):
#     class Meta:
#         model = models.Server
#         fields = '__all__'
#         labels = {
#             'ip':'IP地址',
#             'cpu_number':'CPU大小',
#             'memory':'内存大小(M)',
#             'os':'操作系统',
#             'disk':'磁盘容量(G)',
#             'master_ip':'宿主机IP地址',
#         }

# class AddHostForm(forms.ModelForm):
#     class Meta:
#         model = models.Server
#         fields = '__all__'
#         labels = {
#             'ip':'IP地址',
#             'cpuinfo':'CPU信息',
#             'cpu_number':'CPU大小',
#             'memory':'内存大小',
#             'disk':"磁盘容量",
#         }

class AddUser(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username','full_name','email','password','phone','department','is_admin']
        labels = {
            'username':'用户名',
            'full_name':'真实姓名',
            'email':'邮箱',
            'password':'密码',
            'phone':'电话',
            'department': '部门',
            'is_admin':'管理员',
        }

class AddUserGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = {'name':'用户组名'}