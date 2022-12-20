from django import forms

class NippoFormClass(forms.Form):
    title = forms.CharField(label="タイトル", widget=forms.TextInput(attrs={'placeholder':'タイトル...'}))
    content = forms.CharField(label="内容", widget=forms.Textarea(attrs={'placeholder':'内容...'}))
    
    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs.update({"class":"form-control"})
        super().__init__(*args, **kwargs)