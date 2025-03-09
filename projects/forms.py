from django import forms
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    # Ajout d'une validation pour le champ "title"
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("Le titre doit avoir au moins 3 caractères.")
        return title
    
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Personnaliser le champ description
        }
        
    # Optionnel: Ajout d'une méthode de nettoyage pour personnaliser plus de champs
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("La description doit avoir au moins 10 caractères.")
        return description

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'completed']
        widgets = {
            'completed': forms.CheckboxInput(),  # Personnalisation du champ "completed" avec une case à cocher
        }
    
    # Optionnel: Validation personnalisée pour le champ "title" de Task
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("Le titre de la tâche doit avoir au moins 3 caractères.")
        return title
