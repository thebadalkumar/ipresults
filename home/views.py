from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from .models import Batch, Course, rsFiles, Institute
import json
from .forms import UploadForm, EnrollNum
from django.apps import apps
from rank import DenseRank
import os, re
from django.http import HttpResponse
from django.views.generic import View
from datetime import datetime
#webscrap(ipu notices)
import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
 
#import render_to_pdf from util.py 
from .render import render_to_pdf 

import logging

try:
    db_logger = logging.getLogger('django')
except Exception as err:
    print(str(err))
    
#Creating our view, it is a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        URL = f"http://{request.META['HTTP_HOST']}/result/{request.GET.get('query','00714202018')}/"
        r = requests.get(url = URL)
        pdf = render_to_pdf('home/pdf.html',{'student':r.json(),'time':datetime.now()})
        return HttpResponse(pdf, content_type='application/pdf')

def home(request):
    form = EnrollNum
    return render(request, 'index/home.html',{'form':form})

def search(request):
    form = EnrollNum
    return render(request, 'index/home.html',{'form':form})
# def index(request):
#     return render(request, 'index/index.html')

def result(request):
    return render(request, 'index/index.html')

def ranks(request):
    course = Course.objects.all()
    batch = Batch.objects.all()
    inst = Institute.objects.all()
    context = {
        "course": course,
        "batch": batch,
        "inst": inst
    }
    return render(request, "index/ranks.html", context)
    
def ranks_college_wise(request):
    # change the input values in the template name="code", values="JIMS VK"
    college = request.GET.get('college')
    batch = request.GET.get('batch')
    sem = request.GET.get('sem')
    course = request.GET.get('course')
    ref = request.GET.get('ref')
    institute = Institute.objects.all()
    if not (batch and sem and college and course):
        return render(request, 'home/col-rank.html', {"inst":institute})
    Result = apps.get_model('home', course)
    # filtering using the fields of institute table
    # BCA.objects.filter(institution_code__in=Institute.objects.filter(short="JIMS VK")).distinct()
    if sem=='overall':
        student = Result.objects.filter(institution_code__short=college, batch=batch).annotate(dense_rank=DenseRank("total"))
    if sem=='1':
        student = Result.objects.filter(institution_code__short=college, batch=batch).annotate(dense_rank=DenseRank("sem1_total_marks"))
    if sem=='2':
        student = Result.objects.filter(institution_code__short=college, batch=batch).annotate(dense_rank=DenseRank("sem2_total_marks"))
    if sem=='3':
        student = Result.objects.filter(institution_code__short=college, batch=batch).annotate(dense_rank=DenseRank("sem3_total_marks"))
    if sem=='4':
        student = Result.objects.filter(institution_code__short=college, batch=batch).annotate(dense_rank=DenseRank("sem4_total_marks"))
    if sem=='5':
        student = Result.objects.filter(institution_code__short=college, batch=batch).annotate(dense_rank=DenseRank("sem5_total_marks"))
    if sem=='6':
        student = Result.objects.filter(institution_code__short=college, batch=batch).annotate(dense_rank=DenseRank("sem6_total_marks"))
    # if not student:
    #     context = {'notFound': "We couldn't find the requested ranks"}    
    return render(request, 'home/col-rank.html', {"student":student, "inst_code":college, "course": course, "sem":sem, "inst":institute, "batch":batch, 'ref':ref})

def ranks_university_wise(request):
    batch = request.GET.get('batch')
    sem = request.GET.get('sem')
    course = request.GET.get('course')
    institute = Institute.__namelist__()
    if not (batch and sem and course):
        return render(request, 'home/uni-rank.html')
    Result = apps.get_model('home', course)
    if sem=='overall':
        student = Result.objects.filter(batch=batch).annotate(dense_rank=DenseRank("total"))[:200]
    if sem=='1':
        student = Result.objects.filter(batch=batch).annotate(dense_rank=DenseRank("sem1_total_marks"))[:200]
    if sem=='2':
        student = Result.objects.filter(batch=batch).annotate(dense_rank=DenseRank("sem2_total_marks"))[:200]
    if sem=='3':
        student = Result.objects.filter(batch=batch).annotate(dense_rank=DenseRank("sem3_total_marks"))[:200]
    if sem=='4':
        student = Result.objects.filter(batch=batch).annotate(dense_rank=DenseRank("sem4_total_marks"))[:200]
    if sem=='5':
        student = Result.objects.filter(batch=batch).annotate(dense_rank=DenseRank("sem5_total_marks"))[:200]
    if sem=='6':
        student = Result.objects.filter(batch=batch).annotate(dense_rank=DenseRank("sem6_total_marks"))[:200]
    return render(request, 'home/uni-rank.html', context={"student":student, "sem":sem, "batch":batch, "course":course, "inst":institute})

# about us page request
def aboutus(request):
    return render(request, 'home/about.html')

#notice page request
def getchNotice(request):
    page_number = request.GET.get("page", 1)
    URL = 'http://ggsipu.ac.in/ExamResults/ExamResultsmain.htm'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    u = 'http://ggsipu.ac.in/ExamResults/'
    data = []
    table_body=soup.find('tbody')
    tr = table_body.find_all('tr')[:-1]
    paginator = Paginator(tr, per_page=10)
    rows = paginator.get_page(page_number)
    for row in rows:
        cols = row.find_all('td')
        cols=[x.text.strip() for x in cols]
        title = re.sub('\s+',' ',cols[0])
        date = re.sub('\s+',' ',cols[1])
        links = row.find_all('a')
        for a in links:
            url = u+a['href']
        context = {'title':title, 'url':url, 'date':date}
        data.append(context)
    
    payload = {

        "page": {

            "current": rows.number,

            "has_next": rows.has_next(),

            "has_previous": rows.has_previous(),

        },

        "data": data

    }

    return JsonResponse({'data': payload})

def notice(request):
    page_number = request.GET.get("page", 1)
    URL = 'http://ggsipu.ac.in/ExamResults/ExamResultsmain.htm'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    u = 'http://ggsipu.ac.in/ExamResults/'
    data = []
    table_body=soup.find('tbody')
    tr = table_body.find_all('tr')[:-1]
    paginator = Paginator(tr, per_page=10)
    # rows = paginator.get_page(page_number)
    try:
        rows = paginator.page(page_number)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = paginator.page(paginator.num_pages)

    for row in rows:
        cols = row.find_all('td')
        cols=[x.text.strip() for x in cols]
        title = re.sub('\s+',' ',cols[0])
        date = re.sub('\s+',' ',cols[1])
        links = row.find_all('a')
        for a in links:
            url = u+a['href']
        context = {'title':title, 'url':url, 'date':date}
        data.append(context)
    return render(request, 'home/notices.html', {'data': data, 'page_obj':rows})

# delete the files and the object
def delete_upload(request,pk):
    # if request.user.is_superuser:
    upload = rsFiles.objects.get(pk=pk)
    upload.delete()
    return redirect(upload_list)
    # else:
    #     raise Http404

def edit_upload(request,pk):
    # if request.user.is_superuser:
    upload = rsFiles.objects.get(pk=pk)
    if request.method != 'POST':
        form = UploadForm(instance=upload)
    else:
        form = UploadForm(instance=upload, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_list')
    context = {'form': form}
    return render(request,'home/edit_upload.html', context)
    # else:
    #     raise Http404

# see the list of uploaded files 
def upload_list(request):
    # if request.user.is_superuser:
    uploads = rsFiles.objects.all()
    return render(request, 'home/uploadlist.html', {
        'uploads': uploads
    })
    # else:
    #     raise Http404

# upload the json files (storage)
def upload(request):
    # if request.user.is_superuser:
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        # if form.is_valid():
        #     print("HI")
        form.save()
        return redirect('upload_list')
    else:
        form = UploadForm()
    return render(request, 'home/upload.html', {
        'form': form
    })
    # else:
    #     raise Http404

def acronym(str):
    phrase = (str.replace('OF', '').replace('FOR', '').replace('&', '').replace('AND', '').replace(',','')).split()
    a = ""
    for word in phrase:
        a = a + word[0].upper()
    return a

# inserting into db
def upload_to_db(request,pk):
    file=0
    upload = rsFiles.objects.get(pk=pk)
    # /media/result_pdfs/ to media/result_pdfs
    file = upload.pdf.url[1:]
    # if(upload.migrated == True):
    #     return redirect(upload_list)

    # make it dynamic (course is used to fetch particular modal name)
    # Result = ""
    try:
        Result = apps.get_model('home', upload.course)
        print(Result)
    except (ModuleNotFoundError,LookupError):
        return redirect(upload_list)
        # {err:"Please choose a correct course/ course table doesn't exist"}
    with open(file) as f:
        data = json.load(f)
    for keyval in data:
        # if upload.examination != 'REGULAR ':
        if(keyval["examination_name"] != "REGULAR "):
            roll_number = keyval["roll_num"]
            try:
                q = Result.objects.get(enrollment=roll_number)
                marks = keyval["marks"]
                semester = keyval["semester"]
                
                markss = {
                    semester: {
                        "backlog": {}
                    }
                }
                new_marks = q.semester[str(semester)]["marks"] | marks
                total = 0
                percentage = 0
                data = []
                for s, m in new_marks.items():
                    if m["total"] is None:
                        m["total"] = 0
                    total = total + m["total"]
                    if m["total"] < 40:
                        data.append(m)
                # data = []
                # for s, m in marks.items():
                #     data.append(m)
                backs = q.semester[str(semester)]["backlog"] + data
                percentage = total / len(new_marks.keys())
                markss[semester]["marks"] = new_marks
                markss[semester]["total"] = total
                markss[semester]["backlog"] = backs
                markss[semester]["percentage"] = percentage
                q.semester = q.semester | markss
                q.save(update_fields=['semester'])
                print(roll_number+ " -marks updated")
            except Exception as err:
                print(str(err))
                    
        if upload.examination == 'REGULAR ':
            if (keyval["examination_name"] == 'REGULAR '):
                # batch = keyval["batch"]
                # try:
                #     batch = Batch.objects.get(code=keyval["batch"])
                # except:
                #     make = Batch.objects.create(code = keyval["batch"])
                #     batch = make
                
                batch, created = Batch.objects.get_or_create(batch = keyval["batch"], defaults={'batch': keyval["batch"]})
                
                # try:
                #     course = Course.objects.get(code=keyval["programme_code"])
                #     course.name = keyval["programme_name"]
                #     course.save()
                # except:
                #     make = Course.objects.create(code = keyval["programme_code"])
                #     course = make

                course, created = Course.objects.get_or_create(code = keyval["programme_code"], defaults={'code': keyval["programme_code"], 'name': keyval["programme_name"], 'short': acronym(keyval["programme_name"])})

                marks = keyval["marks"]
                total = 0
                percentage = 0
                data = []
                for s, m in marks.items():
                    if m["total"] is None:
                        m["total"] = 0
                    total = total + m["total"]
                    if m["total"] < 40:
                        data.append(m)

                percentage = total / len(marks.keys())
                # programme_code = Programme.objects.get(code=keyval["programme_code"])
                roll_num = keyval["roll_num"]
                
                semester = keyval["semester"]
                student_name = keyval["student_name"]
                # try:
                #     institution_code = Institute.objects.get(code=keyval["institution_code"])
                # except:
                #     make = Institute.objects.create(code = keyval["institution_code"])
                #     institution_code = make

                institution_code, created = Institute.objects.get_or_create(code = keyval["institution_code"], defaults={'code': keyval["institution_code"], 'name': keyval["institution_name"], 'short': acronym(keyval["institution_name"])})

                result, created = Result.objects.get_or_create(enrollment=roll_num, defaults={'batch': batch, 'institution': institution_code, 'course':course, 'enrollment': roll_num, 'name': student_name})
                if result:
                    markss = {}
                    markss[semester] = {"marks":marks}
                    markss[semester]["total"] = total
                    markss[semester]["backlog"] = data
                    markss[semester]["percentage"] = percentage
                    result.semester = result.semester | markss
                    result.save(update_fields=['semester'])
                    print(roll_num+" - Regular Marks Uploaded")
    return redirect(upload_list)

def add_list_institute(request):
    if request.user.is_superuser:
        file = "media/institute/inst.json"
        # inst = Institute()
        with open(file) as f:
            data = json.load(f)
            for keyval in data:
                name = keyval["name"]
                short = keyval["short"]
                inst, created = Institute.objects.update_or_create(code=keyval["code"], defaults={'name':name, 'short':short})
                # code_list = keyval["code"]
                # for i in code_list:
                #     Institute.objects.update_or_create(code=i, name=keyval["name"], short=keyval["short"])
        return render(request,'index/index.html')
    else:
        raise Http404

def er404(request, exception):
    return render(request,'index/error-404.html',{}, status = 404)

def er500(request):
    return render(request,'index/error-500.html', status = 500)