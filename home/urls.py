from django.urls import path, include
from . import views
from .views import GeneratePdf, ranks
from .api import StudentViewSet, selfcollegeRank, selfuniverityRank, collegeRank, uniRank
urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),
    path('result/', views.result, name="result"),
    # path('col-rank/', views.ranks_college_wise, name="col-rank"),
    # path('uni-rank/', views.ranks_university_wise, name="uni-rank"),
    # path('aboutus/', views.aboutus, name="aboutus"),
    path('notices/', views.notice, name="notice"),
    path('notices/fetch/', views.getchNotice, name="getchNotice"),
    path('upload/', views.upload, name="upload"),
    path('upload/<int:pk>/', views.upload_to_db, name="upload_to_db"), 
    path('upload_list/', views.upload_list, name="upload_list"),
    path('delete_upload/<int:pk>/', views.delete_upload, name="delete_upload"),
    path('edit_upload/<int:pk>/', views.edit_upload, name="edit_upload"),
    path('pdf/', GeneratePdf.as_view(), name="pdf"),
    #path('upload_all/', views.upload_all, name="upload_all"),
    # path('add_inst/', views.add_list_institute, name="add_inst"),

    # New
    path('result/<roll_num>/', StudentViewSet.as_view(), name="student"),
    path('college/rank/<roll_num>/', selfcollegeRank, name="selfcollegeRank"),
    path('college/rank/', collegeRank, name="collegeRank"),
    path('university/rank/<roll_num>/', selfuniverityRank, name="selfuniverityRank"),
    path('university/rank/', uniRank, name="uniRank"),
    path('ranks/',ranks, name="rank")
    # path('index', views.index, name="index")
]

