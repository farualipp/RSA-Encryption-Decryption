from django import forms

class FileEncryptionForm(forms.Form):
    encryption_file = forms.FileField(label='Choose file to encrypt')
    decryption_file = forms.FileField(label='Choose file to decrypt')
