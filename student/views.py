from django.shortcuts import render, redirect
from .models import StudentInfo, StudentDetailInfo, Attendance
from .forms import StudentRegistrationForm, SearchStudentForm, StudentDetailInfoForm, StudentInfoForm


def attendance_count(request):
    class_name = request.GET.get('class_name', None)
    if class_name:
        std_list = StudentDetailInfo.objects.filter(
            std_class__class_short_form=class_name
            ).order_by('roll')
        context = {'std_list': std_list}
    else:
        context = {}
    return render(request, 'student/att_count.html', context)


def search_student(request):
    forms = SearchStudentForm(request.GET or None)
    std_class = request.GET.get('student_class', None)
    section = request.GET.get('section', None)
    std_roll = request.GET.get('roll', None)
    session = request.GET.get('session', None)
    if std_class and section:
        students = StudentDetailInfo.objects.filter(std_class__id=std_class, std_section=section)
        if std_roll:
            students = students.filter(student__roll=std_roll)
        if session:
            students = students.filter(session=session)
        context = {'forms': forms, 'students': students}
        return render(request, 'student/search.html', context)

    context = {'forms': forms}
    return render(request, 'student/search.html', context)


def student_list(request):
    std = StudentDetailInfo.objects.all()
    context = {'students': std}
    return render(request, 'student/student_list.html', context)


def create_student(request):
    forms = StudentRegistrationForm()
    if request.method == 'POST':
        forms = StudentRegistrationForm(request.POST)
        if forms.is_valid():
            std_name = forms.cleaned_data["name"]
            std_age = forms.cleaned_data["age"]
            roll = forms.cleaned_data["roll"]
            std_gender = forms.cleaned_data["gender"]
            fathers_name = forms.cleaned_data["fathers_name"]
            address = forms.cleaned_data["address"]
            std_class = forms.cleaned_data["std_class"]
            std_shift = forms.cleaned_data["std_shift"]
            std_section = forms.cleaned_data["section"]
            session = forms.cleaned_data["session"]

            try:
                std_obj = StudentInfo.objects.create(
                    name=std_name,
                    age=std_age,
                    gender=std_gender,
                    fathers_name=fathers_name,
                    address=address

                )

                StudentDetailInfo.objects.create(
                    student=std_obj,
                    roll=roll,
                    std_class=std_class,
                    std_shift=std_shift,
                    std_section=std_section,
                    session=session
                )
                return redirect('home')
            except Exception as err:
                print("error: ", err)  

    context = {'forms': forms}
    return render(request, 'student/create_std.html', context)


def register_student(request):
    form1 = StudentInfoForm(request.POST or None)
    form2 = StudentDetailInfoForm(request.POST or None)
    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid():
            std_obj = form1.save()
            std_detail = form2.save(commit=False)
            std_detail.student = std_obj
            std_detail.save()
            return redirect('student-list')

    context = {'form1': form1, 'form2': form2}
    return render(request, 'student/register_std.html', context)


def edit_student(request, pk):
    student_detail = StudentDetailInfo.objects.get(id=pk)
    student_info = student_detail.student

    form1 = StudentInfoForm(request.POST or None, instance=student_info)
    form2 = StudentDetailInfoForm(request.POST or None, instance=student_detail)

    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid():
            std_obj = form1.save()
            std_detail = form2.save(commit=False)
            std_detail.student = std_obj
            std_detail.save()
            return redirect('student-list')

    context = {'form1': form1, 'form2': form2}
    return render(request, 'student/edit_std.html', context)

