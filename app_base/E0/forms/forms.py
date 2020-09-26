from django import forms


class ThreadForm(forms.Form):

    name = forms.CharField(label="Name", max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'Anonymous'}), required= False)

    subject = forms.CharField(label="Subject", max_length=50, required = False)

    text = forms.CharField(
        label="Subject", max_length=1000, widget=forms.Textarea, required=True)

    image = forms.ImageField(label="Image", required=False)

    # board = forms.CharField(label = "board", widget= forms.HiddenInput(), required = True)


