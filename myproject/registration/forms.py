from django import forms
from .models import UserDetails, BiometricDetails, Question, Submission, Grade


class UserDetailsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserDetailsForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class BiometricDetailsForm(forms.ModelForm):
    class Meta:
        model = BiometricDetails
        fields = ['facial_scan']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['pdf']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['question', 'answer_pdf']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'feedback']


class CustomLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
