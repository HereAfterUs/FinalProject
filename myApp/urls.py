from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('registry/', views.registry, name='registry'),
    path('logOut/', views.logOut, name='logOut'),
    path('selfInfo/', views.selfInfo, name='selfInfo'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('historyTableData/', views.historyTableData, name='historyTableData'),
    path('addHistory/<int:jobId>', views.addHistory, name='addHistory'),
    path('removeHistory/<int:hisId>', views.removeHistory, name='removeHistory'),
    path('salary/', views.salary, name='salary'),
    path('company/', views.company, name='company'),
    path('educational/', views.educational, name='educational'),
    path('companyStatus/', views.companyStatus, name='companyStatus'),
    path('address/', views.address, name='address'),
    path('recommend/', views.recommend, name='recommend'),
    path('forecast/', views.forecast, name='forecast')
]
