from django.shortcuts import render
from django.http import HttpResponse

import yaml
import os

from django.contrib.auth.decorators import login_required


# VIEWS

@login_required
def index(request):
    return render(request,"main_app/pages/home.html",{})
    # return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def page1(request):
    return render(request, "main_app/pages/page1.html", {})




# METHODS

def getConfig():
    projpath = getProjectPath()
    config = yaml.safe_load(open(projpath + "/project/resources/config/config.yml"))
    return config
    # print(config["xvar"])

def getProjectPath():
    currentfilepath = os.path.abspath(__file__)
    projpath = nthParent(currentfilepath, 2)
    return projpath

def nthParent(path,n):
    result = os.sep.join(path.split(os.sep)[:-n])
    return result
