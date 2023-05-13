from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import StudentSerializer
from .models import BCA, Batch, Institute, Course
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
# For Rank
from django.db.models import F
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from django.apps import apps


class StudentViewSet(APIView):
    serializer_class = StudentSerializer
    # @method_decorator(cache_page(60*60*2))
    def get(self, request, roll_num=None):
        # if id:
        try:
            bot = get_object_or_404(apps.get_model('home', Course.objects.get(code = roll_num[6:9]).short), enrollment=roll_num)
            serializer = self.serializer_class(bot)
        except:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
def collegeRank(request):
    college = request.POST.get("inst",None)
    course = request.POST.get("course", None)
    batch = request.POST.get("batch",None)
    semester = request.POST.get("sem",None)
    student = request.POST.get("student", None)

    objs = {
        "name": [],
        "enroll": [],
        "total": []
    }

    college = Institute.objects.get(code = college)

    model = apps.get_model('home', course)
    if semester == "all":
        obj = model.objects.filter(institution__short=college.short, batch=Batch.objects.get(batch = batch)) #later course will add
        print(obj)
        for stu in obj:
            total = 0
            for sem in stu.semester:
                total += stu.semester[sem]["total"]
            objs["name"].append(stu.name)
            objs["enroll"].append(stu.enrollment)
            objs["total"].append(total) 

    elif semester != "all" and semester is not None:
        obj = model.objects.filter(institution__short=college.short, batch=Batch.objects.get(batch = batch), semester__has_key=semester) #later course will add
        for stu in obj:
            objs["name"].append(stu.name)
            objs["enroll"].append(stu.enrollment)
            objs["total"].append(stu.semester[f'{semester}']["total"])
    else:
        print("Semester is None 404 err")          
    
    df = pd.DataFrame.from_records(objs)
    df["rank"] = df["total"].rank(ascending=False, method="min").astype(int)

    df.sort_values("rank", inplace=True)
    if student:
        df = df[df.eq(student).any(1)]

    return JsonResponse({"tr":[college.name, "Enrollment No.","Name","Total Marks","Rank"],"data":json.loads(df.reset_index().to_json(orient="records"))})

@csrf_exempt
def uniRank(request):
    course = request.POST.get("course", None)
    batch = request.POST.get("batch",None)
    semester = request.POST.get("sem",None)
    student = request.POST.get("student", None)

    objs = {
        "name": [],
        "enroll": [],
        "inst": [],
        "total": []
    }

    model = apps.get_model('home', course)
    
    if semester == "all":
        obj = model.objects.filter(batch=Batch.objects.get(batch = batch)) #later course will add
        for stu in obj:
            total = 0
            for sem in stu.semester:
                total += stu.semester[sem]["total"]
            objs["name"].append(stu.name)
            objs["enroll"].append(stu.enrollment)
            objs["inst"].append(stu.institution.short)
            objs["total"].append(total)  
    elif semester != "all" and semester is not None:
        obj = model.objects.filter(batch=Batch.objects.get(batch = batch),semester__has_key=semester)
        for stu in obj:
            objs["name"].append(stu.name)
            objs["enroll"].append(stu.enrollment)
            objs["inst"].append(stu.institution.short)
            objs["total"].append(stu.semester[f'{semester}']["total"])
    else:
        print("Semester is None 404 err") 
            
    df = pd.DataFrame.from_records(objs)
    df["rank"] = df["total"].rank(ascending=False, method="min").astype(int)

    df.sort_values("rank", inplace=True)
    if student:
        df = df[df.eq(student).any(1)]
    return JsonResponse({"tr":["Enrollment No.","Name","Institution","Total","Rank"],"data":json.loads(df.reset_index().to_json(orient="records"))})

            
# @cache_page(60*60*2)
def selfcollegeRank(request, roll_num):
    model = apps.get_model('home', Course.objects.get(code = roll_num[6:9]).short)
    student = model.objects.get(enrollment=roll_num)
    ranks = {}
    for semester in student.semester:
        collegeRank = model.objects.filter(institution__code=roll_num[3:6], batch=student.batch, semester__has_key=semester).annotate(rank=Window(expression=Rank(),order_by=F(f'semester__{semester}__total').desc()),)
        for self in collegeRank:
            if self.enrollment == roll_num:
                ranks[semester] = self.rank
                break
    
    return JsonResponse(ranks)

# @cache_page(60*60*2)
def selfuniverityRank(request, roll_num):
    model = apps.get_model('home', Course.objects.get(code = roll_num[6:9]).short)
    student = model.objects.get(enrollment=roll_num)
    ranks = {}
    for semester in student.semester:
        collegeRank = model.objects.filter(batch=student.batch, semester__has_key=semester).annotate(rank=Window(expression=Rank(),order_by=F(f'semester__{semester}__total').desc()),)
        for self in collegeRank:
            if self.enrollment == roll_num:
                ranks[semester] = self.rank
                break
    return JsonResponse(ranks)