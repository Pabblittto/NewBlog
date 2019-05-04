from django import forms

class LoginForm(forms.Form):
    UserName= forms.CharField(max_length=150)
    password= forms.CharField(widget=forms.PasswordInput())
    



class RegisterForm(forms.Form):
    UserName= forms.CharField( max_length=150)
    Email = forms.EmailField()
    Password= forms.CharField(
        widget=forms.PasswordInput(),
        label=('Password')

        )
  
    RepeatPassword= forms.CharField(
        widget=forms.PasswordInput(),
        label=('Repeat Password')
    )
    
    def clean_Password(self):
        password1= self.data.get('Password')
        password2 = self.data.get('RepeatPassword')
        if  password1 != password2:
           raise forms.ValidationError("Passwords are not similar")
        return self.cleaned_data.get('Password')