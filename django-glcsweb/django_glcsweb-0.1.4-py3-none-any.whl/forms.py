from django import forms


class CredentialsForm(forms.Form):
    text_input_widget = forms.TextInput(attrs={'class': 'form-control'})
    email_input_widget = forms.EmailInput(attrs={'class': 'form-control'})
    username = forms.CharField(label="Gitlab username", widget=text_input_widget)
    email = forms.CharField(label="Gitlab email", widget=email_input_widget)
    gitlab_token = forms.CharField(label="Gitlab private token", widget=text_input_widget)
    gitlab_server = forms.CharField(label="Gitlab server url", widget=text_input_widget)


class AssignmentsForm(forms.Form):
    TYPE_CHOICES = (
        (0, "Assignment"),
        (1, "Lab"),
    )
    text_input_widget = forms.TextInput(attrs={'class': 'form-control'})
    choice_widget = forms.Select(attrs={'class': 'custom-select'})
    tag_widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. a1'})
    due_date_widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10/25/06 14:59:00'})
    tag = forms.CharField(label="Assignment name/GitLab tag", widget=tag_widget)
    type = forms.ChoiceField(label="Assignment Type", required=False, choices=TYPE_CHOICES, widget=choice_widget)
    due_date = forms.DateTimeField(label="Assignment due date and time", widget=due_date_widget)
    mimir_project_id = forms.CharField(label="Mimir project UUID (can be left blank)", widget=text_input_widget, required=False)


class CourseForm(forms.Form):
    text_widget = forms.TextInput(attrs={'class': 'form-control'})
    textarea_widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    choice_widget = forms.Select(attrs={'class': 'custom-select'})
    ACCESS_CHOICES = (
        (30, "Developer"),
        (40, "Maintainer")
    )
    VISIBILITY_CHOICES = (
        ("private", "private"),
        ("public", "public"),
        ("internal", "internal")
    )
    name = forms.CharField(label="Course name", max_length=10, widget=text_widget)
    semester = forms.CharField(label="Course semester", widget=text_widget)
    mp_id = forms.IntegerField(label="GitLab master project ID", widget=text_widget)
    roster = forms.CharField(label="Course roster", widget=textarea_widget)
    graders = forms.CharField(label="Grader usernames (one per line)", widget=textarea_widget)
    student_access = forms.ChoiceField(label="Student access level", choices=ACCESS_CHOICES, widget=choice_widget)
    grader_access = forms.ChoiceField(label="Grader access level", choices=ACCESS_CHOICES, widget=choice_widget)
    project_visibility = forms.ChoiceField(label="Student project visibility", choices=VISIBILITY_CHOICES, widget=choice_widget)
