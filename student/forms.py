from django import forms
from student.models import StudentProject, ProjectImage


class ProjectImageForm(forms.ModelForm):

    class Meta:
        model = ProjectImage
        fields = ['image' ]

class StudentProjectForm(forms.ModelForm):

    class Meta:
        model = StudentProject
        fields = ['name', 'intro', 'image', 'description', 'tags']