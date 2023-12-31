from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from datetime import date
import json
from baseApp.models import Admins_details, Aunthaticate, Typing_testing, Variant_paragraphs
from topApp.views import id_gen
import random


def ttd_admin_login(request):
    return render(request, 'ttd_admin_login.html')


def ttd_admin_signin(request):
    return render(request, 'ttd_admin_signin.html')


def ttd_admin_homepage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        details = Admins_details.objects.filter(
            emails=username, passw=password)
        if details.exists():
            date1 = datetime.now()
            admin_details = details.values()
            admin_details2 = Admins_details.objects.all().values()
            amount_of_admins = len(admin_details2)
            return render(request, 'ttd_admin_homepage.html', {
                'admin_details': admin_details,
                'admin_details2': admin_details2,
                'date1': date1,
                'amount_of_admins': amount_of_admins
            })
        else:
            return HttpResponse("Failed to connect")
    return redirect('ttd_admin_login')


def paragraph():
    paragraphs = Typing_testing.objects.all()
    for paragraph in paragraphs:
        splitedParagraph = paragraph.test.split()
        random.shuffle(splitedParagraph)
        joinedParagraph = " ".join(splitedParagraph)

        vps = Variant_paragraphs.objects.filter(variant_id=paragraph.test_id)
        if vps.exists():
            for vp in vps:
                vp.variant_p = joinedParagraph
                vp.save()
        else:
            vp = Variant_paragraphs.objects.create(
                variant_p=joinedParagraph, variant_id=paragraph.test_id)


def get_paragraph(request):
    paragraphs = Variant_paragraphs.objects.all()
    return JsonResponse({"paragraphs": list(paragraphs.values())})

def get_typing_tests(request):
    typing_testing = Typing_testing.objects.all()
    return JsonResponse({"Typing_testings": list(typing_testing.values())})

def get_typing_variants(request):
    variant_paragraphs = Variant_paragraphs.objects.all()
    return JsonResponse({"variant_paragraphs": list(variant_paragraphs.values())})

def typing_tests(request):
    if request.method == 'POST':
        tests = json.loads(request.body)
        textarea = tests['textarea2']
        id = id_gen()
        count = textarea.split()
        get_all_paragraphs = Typing_testing.objects.all().values()
        amount_of_paragraphs = len(get_all_paragraphs)
        if len(count) > 20 :
            if len(count) <= 50 :
                if amount_of_paragraphs < 10 :
                    paragraphs = Typing_testing.objects.create(test = textarea, test_id =id)
                    paragraphs.save()
                    return HttpResponse('SAVED SUSSESSIFULLY....')
                else:
                    return HttpResponse('YOU HAVE REACHED MAXMUM AMOUT OF PARAGRAPHS..')
            else:
                return HttpResponse('TEST PARAGRAPH SHOULD NOT EXCEED 50 WORDS.')
        else:
            return HttpResponse('TEST PARAGRAPH SHOULD BE GREATER THAN 20 WORDS.')
    else:
        return HttpResponse('SOMETHING WENT WRONG..')

def delete_paragraphs(request):
    if request.method == "POST":
        data = json.loads(request.body)
        checked_array = data.get("checkedArray", [])
        for paragraph_id in checked_array:
            Typing_testing.objects.filter(test_id=paragraph_id).delete()
            Variant_paragraphs.objects.filter(variant_id=paragraph_id).delete()
        return HttpResponse("DELETED SUCCESSIFULLY")
    
def delete_variants(request):
    if request.method == "POST":
        data = json.loads(request.body)
        checked_array = data.get("checkedArray", [])
        for paragraph_id in checked_array:
            Variant_paragraphs.objects.filter(variant_id=paragraph_id).delete()
        return HttpResponse("VARIANTS DELETED SUCCESSIFULLY")

