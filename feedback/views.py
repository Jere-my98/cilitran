# Create your views here.
# This file is the requests-handler for this app
# Every Data exchange between client and server involves a request and a response

from django.shortcuts import render
from django.http import HttpResponse

# A View function is a function that takes in a request and returns a response. It may also be called a request-handler or action
# If, in the view functions, you are not returning a plain HTML text but a whole HTTP file, we use 'render' function from 'django.shortcuts' and not 'HttpResponse' from 'django.http'

def say_hello(request):
    x = 1
    y = 2
    return render(request,'hello.html',{'name':'Jeremy'})

