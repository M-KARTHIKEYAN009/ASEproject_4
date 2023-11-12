from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ElectionUser

class ElectionUserCreationForm(UserCreationForm):
    username = forms.CharField(required=False, help_text='Your phone number will be your admin username',label="Personal Phone Number")

    #is_superuser = forms.BooleanField(label="Is Admin")
    class Meta:
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        model = ElectionUser
        fields = ('username','first_name','last_name','email','dob','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ElectionUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        #self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ElectionUser


class ElectionVoterCandidateCreationForm(forms.ModelForm):
    phone = forms.CharField(required=False, help_text='Your phone number will be your primary contact',
                            label="Personal Phone Number")
    class Meta:
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        model = ElectionUser
        fields = ('username', 'first_name', 'last_name','dob' ,'email', 'phone', 'is_candidate', 'is_voter')

    def __init__(self, *args, **kwargs):
        super(ElectionVoterCandidateCreationForm, self).__init__(*args, **kwargs)
        # Update the form's widgets
        for fieldname in ['username', 'email', 'first_name', 'last_name', 'phone']:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
        for fieldname in ['is_candidate', 'is_voter']:
            self.fields[fieldname].widget.attrs.update({'class': 'checkbox'})

    def save(self, commit=True):
        user = super(ElectionVoterCandidateCreationForm, self).save(commit=False)
        if commit:
            # Since we're not including password fields, you may want to set a default password
            # and force the user to change it on first login, or send them an email with a token to set the password.
            user.set_unusable_password()
            user.save()
        return user


from .models import ElectionEvent

class ElectionEventForm(forms.ModelForm):
    class Meta:
        model = ElectionEvent
        fields = '__all__'
        widgets = {
            'date_of_election': forms.DateInput(attrs={'type': 'date'}),
            'voting_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'voting_end_time': forms.TimeInput(attrs={'type': 'time'}),
            'result_announcement_date': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['has_concluded', 'victor']  # Excluding fields not needed during creation



from django.core.exceptions import ValidationError
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # widgets = {
        #     'dob': forms.DateInput(attrs={'type': 'date'}),
        # }
        fields = ['gender', 'residence', 'party', 'id_document', 'biography']

    def clean(self):
        cleaned_data = super().clean()
        # if self.instance.account.is_candidate is False and :
        #     raise ValidationError("Only candidates can update these details.")
        return cleaned_data

class VoterUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # widgets = {
        #     'dob': forms.DateInput(attrs={'type': 'date'}),
        # }
        fields = ['gender', 'residence', 'id_document', 'biography']

    def clean(self):
        cleaned_data = super().clean()
        # if self.instance.account.is_candidate is False and :
        #     raise ValidationError("Only candidates can update these details.")
        return cleaned_data