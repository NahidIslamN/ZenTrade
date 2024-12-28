

from django.shortcuts import render, redirect
from django.views import View


###Write your View here


class HomePage(View):
    def get(self,request):

        return render(request,'pub/index.html')
    

class AboutPage(View):
    def get(self,request):

        return render(request,'pub/about.html')

class ContactPage(View):
    def get(self,request):

        return render(request,'pub/contact.html')