from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','email','age','city']

    def clean_name(self):
        n = self.cleaned_data.get('name','').strip()
        if len(n) < 3:
            raise
        forms.ValidationError("Name must have at least 3 characters.")
        return n
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age <= 0:
            raise
        forms.ValidationError("Age must be positive.")
        return age

      