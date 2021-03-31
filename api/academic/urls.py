from django.urls import path

from . import views


urlpatterns = [
    path('upload-statistics/<str:plan_study>/',
         views.FileAcademicStatisticsView.as_view(), name='upload-statistics'),

    path('list-statistics/<str:plan>/<str:departament>/<int:year>/<str:trimester>/',
         views.AcademicStatisticsView.as_view(), name='list-statistics'),
    path('list-statistics-totals/<str:plan>/<str:departament>/<int:year>/',
         views.AcademicStatisticsTotalsView.as_view(), name='list-statistics-totals'),
    path('list-filter-course/<str:number>/<str:course>/',
         views.AcademicStatisticsFilterCourseView.as_view(), name='list-filter-course'),
    path('create-statistics/',
         views.CreateAcademicStaticsView.as_view(), name='create_statics'),
    path('list-departament/',
         views.ListDepartamentView.as_view(), name='list_departament'),
    path('list-study-plan/',
         views.ListStudyPlanView.as_view(), name='list_study_plan'),
    path('list-years/',
         views.ListYears.as_view(), name='list_years'),
    path('list-course/<str:filter>/',
         views.CourseView.as_view(), name='list_course'),
    path('update-academic/<int:pk>/',
         views.UpdateAcademicStaticsView.as_view(), name='update_statics'),
    path('retrieve-academic/<int:pk>/',
         views.RetrieveAcademicStaticsView.as_view(), name='update_statics'),
    path('list-history-acadedic-for-user/',
         views.ListHistoryAcademicForUser.as_view(), name='list-history-academic-for-user'),

    path('list-history-academic-for-user-and-for-year/<int:year>/',
         views.ListHistoryAcademicForUserAndForYear.as_view(),
         name='list-history-academic-for-user-and-for-number'),

    path('list-multi-totals/<str:plans>/<str:departament>/<str:initial>/<str:final>/',
         views.ListTotalsMultiPlans.as_view(), name='list-multi-plans'),

    path('users/', views.UserPrivilegesAcademicView.as_view(), name='privileges_users'),
    path('user/<int:pk>/', views.DeletePrivilegeUserView.as_view(), name='delete-privilege'),
    path('list-users/', views.ListUserPrivilegesAcademicView.as_view(), name='list_users')
]
