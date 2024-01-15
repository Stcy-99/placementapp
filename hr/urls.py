from django.urls import path
from hr import views

urlpatterns=[
    path("",views.SignInView.as_view(),name="sign-in"),
    path("index",views.DashboardView.as_view(),name="index"),
    path("signout",views.SignOutView.as_view(),name="signout"),
    path("category",views.CategoryListCreateView.as_view(),name="category"),
    path("category/<int:pk>/remove",views.CategoryDeleteView.as_view(),name="category-remove"),
    path("jobs/add",views.JobCreateView.as_view(),name="job-add"),
    path("jobs/all",views.JobListView.as_view(),name="job-list"),
    path("jobs/<int:pk>/remove",views.JobDeleteView.as_view(),name="job-delete"),
    path("jobs/<int:pk>/change",views.JobUpdateView.as_view(),name="job-edit"),
    path("jobs/<int:pk>/applications",views.JobApplicationListView.as_view(),name="job-applicationlist"),
    path("applications/<int:pk>/",views.ApplicationDetailView.as_view(),name="job-applicationdetail"),
    path("applications/<int:pk>/change/",views.ApplicationUpdateView.as_view(),name="job-applicationedit")





]

