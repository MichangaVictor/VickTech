from student_management_app.forms import AddStudentForm, EditStudentForm
from django.contrib import messages
from student_management_app.models import Courses, CustomUser, SessionYearModel, Staffs, Students, Subjects
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.urls import reverse



def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    return render(request,"hod_template/add_staff.html")

def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return HttpResponse('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            student = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            student.staffs.address = address
            student.save()
            messages.success(request, "Staff Added Successfully!")
            return HttpResponseRedirect(reverse('add_staff'))
        except:
            messages.error(request, "Failed to Add Staff!")
            return HttpResponseRedirect(reverse('add_staff'))

def add_course(request):
    return render(request,"hod_template/add_course.html")


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return HttpResponse('add_course')
    else:
        course = request.POST.get('course')        

        try:
            course_model = Courses(course_name=course)
            course_model.save()            
            messages.success(request, "Course Added Successfully!")
            return HttpResponseRedirect(reverse('add_course'))
        except:
            messages.error(request, "Failed to Add Course!")
            return HttpResponseRedirect(reverse('add_course'))

def add_student(request):    
     
    # student=Students.objects.get(admin=student_id)
    # return render(request,"hod_template/add_student.html",{"student": student,"courses": courses})
     form=AddStudentForm()
     return render(request,"hod_template/add_student.html",{ "form": form})


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return HttpResponse('add_student')
        
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']        
            session_year_id= form.cleaned_data['session_year_id']
            course_id= form.cleaned_data['course_id']
            gender= form.cleaned_data['gender']
            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                student = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                student.Students.address = address

                course_obj = Courses.objects.get(id=course_id)
                student.Students.course_id = course_obj

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                student.Students.session_year_id = session_year_obj

                student.Students.gender = gender
                student.Students.profile_pic = profile_pic_url
                student.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            form= AddStudentForm(request.POST)
            #return render(request,"hod_template/add_student.html",{"form": form})
            return render(request,"hod_template/add_student.html",{"form": form})


def add_subject(request):
    courses = Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject.html",{"staffs": staffs,"courses": courses})

def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method Not Allowed </h2>")

    else:
        subject_name= request.POST.get('subject_name')
        course_id=request.POST.get('course')
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get('staff')  
        staff=CustomUser.objects.get(id=staff_id) 

        try:
            subject = Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return HttpResponseRedirect(reverse('add_subject')) 

        except:
            messages.error(request, "Failed to Add Subject!")
            return HttpResponseRedirect(reverse('add_subject'))

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs})

def manage_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/manage_student.html",{"students":students})

def manage_course(request):
    courses=Courses.object.all()
    return render(request,"hod_template/manage_course.html",{"courses":courses}) 

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})        

def edit_staff(request, staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff.html",{"staff":staff, "id":staff.id}) 


def edit_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return HttpResponse('edit_staff')
    else:
        staff_id= request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')        
        address = request.POST.get('address')

        try:

          student=CustomUser.objects.get(id=staff_id)
          student.first_name=first_name
          student.last_name=last_name
          student.email=email
          student.username=username
          student.save()

          staff_model=Staffs.objects.get(admin=staff_id)
          staff_model.address=address
          staff_model.save()

          messages.success(request, "Successfully Editted Staff!")
          return HttpResponseRedirect(reverse('edit_staff', kwargs={'staff_id':staff_id}))


        except:
            messages.error(request, "Failed to Edit Staff!")
            return HttpResponseRedirect(reverse('edit_staff', kwargs={'staff_id':staff_id}))

def edit_student(request, student_id):    
    request.session['student_id'] = student_id
    student=Students.objects.get(admin=student_id)
    form= EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['gender'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id    
    return render(request,"hod_template/edit_student.html",{ "form":form, "id":student.id, "username":student.admin.username}) 

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:  
        student_id=request.session.get('student_id')
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']    
            address = form.cleaned_data['address']
            session_year_id= form.cleaned_data['session_year_id']            
            course_id= form.cleaned_data['course']
            gender= form.cleaned_data['gender']

            if request.FILES.get('profile_pic',False):
                profile_pic = request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None    

            try:
                student= CustomUser.objects.get(id=student_id)
                student.first_name=first_name
                student.last_name=last_name
                student.username=username
                student.email=email
                student.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                session_year=SessionYearModel.object.get(id=session_year_id)
                student.students.session_year_id=session_year                
                student.gender=gender        
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url != None:
                  student.profile_pic=profile_pic_url           
                student.save()
                del request.session['student_id']
                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id': student_id}))

            except:
                messages.error(request, "Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id': student_id}))
        else:
            form=EditStudentForm(request.POST)  
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student.html",{"form":form,"id":student_id, "username":student.admin.username})      

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type='2')
    return render(request,"hod_template/edit_subject.html",{ "subject":subject ,  "staffs":staffs ,"courses": courses , "id":subject_id }) 



def edit_subject_save(request):
    
     if request.method != "POST":
         messages.error(request, "Invalid Method ")
         return HttpResponse('edit_subject')

     else:
         subject_id= request.POST.get('subject_id')
         subject_name = request.POST.get('subject_name')
         staff_id= request.POST.get('staff')
         course_id= request.POST.get('course')

         try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course                        
            subject.save()
            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={'subject_id': subject_id}))
         except:
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={'subject_id': subject_id}))
    



def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course.html",{ "course":course, "id":course.id})



def edit_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return HttpResponse('edit_course')

    else:
        course_id= request.POST.get('course_id')
        course_name = request.POST.get('course')

        try:
           course=Courses.objects.get(id=course_id)
           course.course_name=course_name
           course.save()
           messages.success(request, "Successfully Edited Course")
           return HttpResponseRedirect(reverse("edit_course", kwargs={'course_id':course_id}))
        except:
           messages.error(request, "Failed to Edit Course")
           return HttpResponseRedirect(reverse("edit_course", kwargs={'course_id':course_id}))  
        

def manage_session(request):
    return render(request,"hod_template/manage_session.html")

def add_session_save(request): 
    if request.method != "POST":
        return HttpResponseRedirect(reverse('manage_session'))
    else:
        session_start_year= request.POST.get('session_start')
        session_end_year=request.POST.get('session_end')
        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year) 
            sessionyear.save() 
            messages.success(request, "Successfully Added Session Year")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
           messages.error(request, "Failed to Add Course")
           return HttpResponseRedirect(reverse("manage_session")) 



   



    




