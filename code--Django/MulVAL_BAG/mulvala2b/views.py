from django.shortcuts import render, redirect
from django.urls import reverse

from mulvala2b import models
from mulvala2b.src.A2B import A2B, aimSel
from django.shortcuts import HttpResponse
import os
import shutil


# Create your views here.

def window(req):
    return render(req, "index.html")


def mulval(req):
    shutil.rmtree('./mulvala2b/src/mulvalsrc')
    os.mkdir('./mulvala2b/src/mulvalsrc')
    print("前端数据: ", req.POST)
    print("file:", req.FILES)
    if req.method == "POST":
        file = req.FILES.get("upload", None)
        if not file:
            return render(req, "index.html", {"errinf":"No files for upload!"})
        f = open("./mulvala2b/src/mulvalsrc/input.P", 'wb')
        for line in file.chunks():      # 分块写入
            f.write(line)
        f.close()
    root = os.getcwd()
    path = root + "/mulvala2b/src/mulvalsrc"
    if os.system("cd "+ path + " && ls && graph_gen.sh input.P -v"):
        return redirect('/mulval/mulvalerror1/')
    elif os.path.exists('./mulvala2b/src/mulvalsrc/AttackGraph.pdf'):
        return redirect('/mulval/mulvalsuccess/')
    else:
        return redirect('/mulval/mulvalerror2/')

def mulvalerror1(req):
    return render(req, "index.html", {"errinf":"Wrong file! Please check your file type or grammer."})

def mulvalsuccess(req):
    aimlist = aimSel()
    return render(req, "index.html", {"goodnews": "An AG was generated successfully.", "retcode": 1, "aimlist": aimlist})

def mulvalerror2(req):
    return render(req, "index.html", {"errinf": "No attack path find."})


def download(req):
    if os.path.exists('./mulvala2b/src/mulvalsrc/AttackGraph.pdf'):
        pdfFileObj = open('./mulvala2b/src/mulvalsrc/AttackGraph.pdf', 'rb')
        response = HttpResponse(pdfFileObj.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="AttackGraph.pdf"'
        return response



def a2b(req):
    if req.method == "POST":
        aim = req.POST.get("Attack Goal", None)
        print(aim)
        A2B(aim)
        if os.path.exists('./mulvala2b/src/mulvalsrc/result.dot.pdf'):
            pdfFileObj = open('./mulvala2b/src/mulvalsrc/result.dot.pdf', 'rb')
            response = HttpResponse(pdfFileObj.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="BAG.pdf"'
            return response
        else:
            return redirect('/mulval/a2berror/')

def a2berror(req):
    aimlist = aimSel()
    return render(req, "index.html",{"goodnews": "An AG was generated successfully.", "a2berror": "No attack path to this target!", "retcode": 1, "aimlist": aimlist})