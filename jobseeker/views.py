from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from django.views.generic import View,CreateView,TemplateView,DetailView,UpdateView,ListView
from myapp.models import StudentProfile,Jobs,Applications,Category
from jobseeker.forms import RegistrationForm,ProfileForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages





def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"signin required")
            return redirect("sign-in")
        else:
            return fn(request,*args,**kwargs)    
    return wrapper

decs=[signin_required,never_cache]
    

class SignUpView(CreateView):
    template_name="jobseeker/register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("sign-in")

# @method_decorator(decs,name="dispatch")

@method_decorator(decs,name="dispatch")
class StudentIndexView(ListView):
    template_name="jobseeker/index.html"
    context_object_name="data"
    model=Jobs
    def get_queryset(self):
        my_application=Applications.objects.filter(student=self.request.user).values_list("job",flat=True)
        
        qs=Jobs.objects.exclude(id__in=my_application).order_by("created_date")
        # localhost8000/seeker/index/?category=frontend
        if "category" in self.request.GET:
            category_value=self.request.GET.get("category")
            qs=qs.filter(category__name=category_value)
            print(category_value)
        return qs
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        qs=Category.objects.all()
        context["categories"]=qs
        return context


    
@method_decorator(decs,name="dispatch") 
class ProfileCreateView(CreateView):
    template_name="jobseeker/profile_add.html"
    form_class=ProfileForm
    success_url=reverse_lazy("seeker_index")
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)


@method_decorator(decs,name="dispatch")
class ProfileDetailView(DetailView):
    template_name="jobseeker/profile_detail.html"
    context_object_name="data"
    model=StudentProfile


@method_decorator(decs,name="dispatch")
class ProfileEditView(UpdateView):
    template_name="jobseeker/profile_edit.html"
    form_class=ProfileForm
    model=StudentProfile
    success_url=reverse_lazy("seeker_index")


@method_decorator(decs,name="dispatch")
class JobListView(ListView):
    template_name="jobseeker/job_list.html"
    context_object_name="jobs"
    model=Jobs
     

@method_decorator(decs,name="dispatch")
class JobDetailView(DetailView):
    template_name="jobseeker/job_detail.html"
    model=Jobs
    context_object_name="data"


@method_decorator(decs,name="dispatch")
class ApplyJobView(View) :
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        user_object=request.user
        Applications.objects.create(job=job_object,student=user_object)
        return redirect("seeker_index")


@method_decorator(decs,name="dispatch") 
class ApplicationListView(ListView):
    template_name="jobseeker/application.html"
    model=Applications
    context_object_name="data"

    def get_queryset(self):
        qs=Applications.objects.filter(student=self.request.user)
        return qs
    

@method_decorator(decs,name="dispatch")
class JobSaveView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        action=request.POST.get("action")
        if action=="save":
            request.user.profile.saved_job.add(job_object)
        elif action=="unsave":
            request.user.profile.saved_job.remove(job_object)
        return redirect("seeker_index")
    

@method_decorator(decs,name="dispatch")    
class SavedJobsListView(View):
    template_name="jobseeker/saved_jobs.html"
    model=StudentProfile
    def get(self,request,*args,**kwargs):
        qs=request.user.profile.saved_job.all()
        return render(request,self.template_name,{"data":qs})

    

