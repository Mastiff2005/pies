from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class CreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ('username', 'organization', 'email', 'phone', 'address')
