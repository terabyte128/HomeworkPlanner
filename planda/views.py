from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http.response import HttpResponse, HttpResponseRedirect

from planda.models import Assignment, Course

# Create your views here.


def index(request):
    if not request.user.is_authenticated():
        return render(request, "planda/login.html")
    else:

        context = {
            'user': request.user
        }
        return render(request, "planda/index.html", context)


def login_user(request):
    if not request.user.is_authenticated():
        if request.POST.get("username") and request.POST.get("password"):

            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    messages.error(request, "Your account is inactive.")
            else:
                messages.error(request, "Your account does not exist, or your credentials were incorrect.")

        else:
            messages.error(request, "Your session timed out, please login again.")

    return HttpResponseRedirect(reverse('planda:index'))


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return HttpResponseRedirect(reverse('planda:index'))


@login_required
def assignments(request):
    user = request.user

    courses = Course.objects.filter(user=user)

    course_list = []

    for course in courses:
        assignments = Assignment.objects.filter(course=course)

        assignment_list = {
            'course_name': course.name,
            'assignments': assignments
        }

        course_list.append(assignment_list)

    context = {
        'course_list': course_list,
    }

    return render(request, "planda/assignments.html", context)


@login_required
def assignment_detail(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        messages.error(request, "Assignment not found.")
        return HttpResponseRedirect(reverse('planda:assignments'))

    # are they allowed to view?
    if assignment.course.user == request.user:
        context = {
            'assignment': assignment,
        }
        return render(request, "planda/single_assignment.html", context)

    else:
        messages.error(request, "Assignment not found.")
        return HttpResponseRedirect(reverse('planda:assignments'))

@login_required
def courses(request):
    pass