from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

from django.contrib.auth.models import User
from models import *

class RegistrationForm(forms.Form):
	email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}))
	username = forms.CharField(max_length = 200,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))	
	password1 = forms.CharField(max_length = 20, 
								widget = forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}))
	password2 = forms.CharField(max_length = 20,  
								widget = forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm Password'}))

	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(RegistrationForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		# Generally return the cleaned data we got from our parent.
		return cleaned_data

	def clean_username(self):
		# Confirms that the username is not already present in the
		# User model database.
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

		# Generally return the cleaned data we got from the cleaned_data
		# dictionary
		return username

class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))

	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(LoginForm, self).clean()

		# Confirms that the two password fields match
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')

		# Generally return the cleaned data we got from our parent.
		return cleaned_data
		
# log in user change password
class LoginChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(max_length = 20, 
								widget = forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password1 = forms.CharField(max_length = 20, 
								widget = forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password2 = forms.CharField(max_length = 20, 
								widget = forms.PasswordInput(attrs={'class': 'form-control'}))

# enter the email for setting password
class EmailResetPasswordForm(PasswordResetForm):
	email = forms.EmailField(max_length = 200, 
								widget = forms.TextInput(attrs={'class': 'form-control'}))


# reset password by the email link
class EmailResetPasswordConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(max_length = 20, 
								widget = forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password2 = forms.CharField(max_length = 20, 
								widget = forms.PasswordInput(attrs={'class': 'form-control'}))


class IntroForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('intro',)
		widgets = {
			'intro': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please introduce yourself.'}),
		}

class PhotoForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('photo',)
		widgets = {
			'photo': forms.FileInput(attrs={'class': 'form-control btn btn-sm btn-info choose-photo'}),
		}


class ReviewForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ReviewForm, self).__init__(*args, **kwargs)
		self.fields['text'].label = 'Content'
	
	class Meta:
		model = Review
		fields = ('title', 'text')
		
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'text': forms.Textarea(attrs={'class': 'form-control','rows': 5}),
		}


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)
		widgets = {
			'text': forms.TextInput(attrs={'class': 'form-control'}),
		}


class SearchForm(forms.Form):
    search_content = forms.CharField(max_length=42,
                widget = forms.TextInput(attrs = \
                {'class' : 'form-control',
                'name' : 'keyword',
                'placeholder' : 'Search...'}))
    search_type = forms.ChoiceField(choices = \
                [('all', 'All'), ('movies', 'Movies'), ('names', 'Names'), ('users', 'Users')], 
                widget = forms.Select(attrs = {'name':"search_type"}),
                initial = 'all')
