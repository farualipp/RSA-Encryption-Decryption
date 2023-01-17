from inspect import signature
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse , FileResponse
import rsa
import os
from .models import RSAKey

# Create your views here.
def login(request):
     return render(request , "login/index.html")

def signin(request):
            if request.method == "POST":
                    username = request.POST['username']
                    password = request.POST['password']
                    if username == 'admin'and password == 'admin':
                            return redirect ('home')
                    else :
                         messages.info(request, 'Username or password is incorrect')
            return render(request, 'login/signin.html')



def home(request):  
        if request.method == 'POST':
           if 'encrypt' in request.POST:
            # handle the file upload
            file = request.FILES['encryption_file']
            # generate the RSA key pair
            (pubkey, privkey) = rsa.newkeys(512)
            # save the RSA key pair to a file
            with open(os.path.join('keys', 'private_key.pem'), 'wb') as f:
                f.write(privkey.save_pkcs1())
            with open(os.path.join('keys', 'public_key.pem'), 'wb') as f:
                f.write(pubkey.save_pkcs1())
            # encrypt the file
            plaintext = file.read()
            ciphertext = rsa.encrypt(plaintext, pubkey)
            # write the encrypted file
            with open(file.name + '.txt', 'wb') as f:
                f.write(ciphertext)
            # create the file response to download the encrypted file
            response = FileResponse(open(file.name + '.txt', 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + file.name + '.txt'
            return response
           elif 'decrypt' in request.POST:
            # handle the file upload
            file = request.FILES['encryption_file']
            # load the RSA key pair from the file
            with open(os.path.join('keys', 'private_key.pem'), 'rb') as f:
                privkey = rsa.PrivateKey.load_pkcs1(f.read())
            # decrypt the file
            ciphertext = file.read()
            plaintext = rsa.decrypt(ciphertext, privkey).decode()
            # write the decrypted file
            with open(file.name + '.dec', 'w') as f:
                f.write(plaintext)
            # create the file response to download the decrypted file
            response = FileResponse(open(file.name + '.dec', 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + file.name + '.txt'
            return response
        return render(request, 'login/home.html')