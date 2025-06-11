from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):

    class Meta:
        model= User
        fields=("username","email","password1","password2")

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["email"].label="Email Address"
