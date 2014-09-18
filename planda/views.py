from datetime import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http.response import HttpResponse, HttpResponseRedirect, Http404

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


# Assignment views

@login_required
def assignments(request):

    if 'assignmentName' in request.POST:
        return assignment_add(request)

    user = request.user

    courses = Course.objects.filter(user=user).order_by('period')

    course_list = []

    for course in courses:
        assignments = Assignment.objects.filter(course=course).order_by('due_date')

        assignment_wrapper = []

        for assignment in assignments:
            overdue = (assignment.due_date <= datetime.now().date()) and not assignment.completed

            # sorry, future self
            # if not (not overdue and assignment.due_date < datetime.now().date()):

            if overdue or (assignment.due_date <= datetime.now().date() and not assignment.completed):

                single_wrapper = {
                    'name': assignment.name,
                    'id': assignment.id,
                    'description': assignment.description,
                    'due_date': assignment.due_date,
                    'completed': assignment.completed,
                    'overdue': overdue
                }

                assignment_wrapper.append(single_wrapper)

        assignment_list = {
            'course_name': course.name,
            'assignments': assignment_wrapper
        }

        course_list.append(assignment_list)

    context = {
        # raw course objects (for form)
        'courses': courses,

        # list with assignments
        'course_list': course_list,
    }

    return render(request, "planda/assignments.html", context)


@login_required
def assignment_detail(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        raise Http404

    # are they allowed to view?
    if assignment.course.user == request.user:
        context = {
            'assignment': assignment,
            'due_date': assignment.due_date.strftime("%Y-%m-%d")
        }
        return render(request, "planda/single_assignment.html", context)

    else:
        raise Http404

@login_required
def assignment_toggle_completed(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)

        # are they allowed to view?
        if assignment.course.user == request.user:
            assignment.completed = not assignment.completed

            assignment.save()

            is_completed = assignment.completed

            response = {
                'changed': True,
                'completed': is_completed
            }

        else:
            response = {
                'changed': False,
                'completed': False
            }

    except Assignment.DoesNotExist:

        response = {
            'changed': False,
            'completed': False
        }

    return HttpResponse(json.dumps(response), content_type="application/json")


def assignment_delete(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)

        # are they allowed to view?
        if assignment.course.user == request.user:

            assignment.delete()

            response = {
                'deleted': True,
            }

        else:
            response = {
                'deleted': False,
                'reason': "NotAllowed"
            }

    except Assignment.DoesNotExist:

        response = {
            'deleted': False,
            'reason': "DoesNotExist"
        }

    # return HttpResponse(json.dumps(response), content_type="application/json")

    # if not response['deleted']:
        # messages.error(request, "An error occured while deleting your assignment: " + response['reason'])

    return HttpResponseRedirect(reverse('planda:assignments'))


@login_required
def assignment_edit(request):
    name = request.POST['name']
    pk = request.POST['pk']
    value = request.POST['value']

    assignment = Assignment.objects.get(id=pk)

    if assignment.course.user == request.user:
        setattr(assignment, name, value)
        assignment.save()

        return HttpResponse(status=200)


@login_required
def assignment_add(request):
    if 'assignmentName' in request.POST:
        name = request.POST['assignmentName']
        description = request.POST['assignmentDescription']
        due_date = request.POST['assignmentDueDate']
        course = request.POST['assignmentCourse']

        new_assignment = Assignment(name=name, description=description, due_date=due_date, course=Course.objects.get(id=course))

        new_assignment.save()

    return HttpResponseRedirect(reverse('planda:assignments'))


# Course Views

def courses(request):
    try:
        courses = Course.objects.filter(user=request.user)

    except Course.DoesNotExist:
        courses = []

    context = {
        'courses': courses
    }

    return render(request, 'planda/courses.html', context)


def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)

        if request.user != course.user:
            raise Http404

        context = {
            'course': course,
            # 'assignment_number': len(course.assignment_set)
        }

        return render(request, 'planda/single_course.html', context)

    except Course.DoesNotExist:
        raise Http404


@login_required
def course_edit(request):
    name = request.POST['name']
    pk = request.POST['pk']
    value = request.POST['value']

    try:
        course = Course.objects.get(id=pk)

        if course.user == request.user:
            setattr(course, name, value)
            course.save()

            return HttpResponse(status=200)

    except Course.DoesNotExist:
        return Http404

@login_required
def course_delete(request, course_id):
    try:
        course = Course.objects.get(id=course_id)

        # are they allowed to view?
        if course.user == request.user:

            course.delete()

            response = {
                'deleted': True,
            }

        else:
            response = {
                'deleted': False,
                'reason': "NotAllowed"
            }

    except Course.DoesNotExist:

        response = {
            'deleted': False,
            'reason': "DoesNotExist"
        }

    # return HttpResponse(json.dumps(response), content_type="application/json")

    # if not response['deleted']:
        # messages.error(request, "An error occured while deleting your assignment: " + response['reason'])

    return HttpResponseRedirect(reverse('planda:courses'))


def course_add(request):
    if 'courseName' in request.POST:
        name = request.POST['courseName']
        description = request.POST['courseDescription']
        period = request.POST['coursePeriod']

        new_course = Course(user=request.user, name=name, description=description, period=period)

        new_course.save()

    return HttpResponseRedirect(reverse('planda:courses'))


# Preferences


def preferences(request):
    return render(request, 'planda/preferences.html')


# Create account

def create_account(request):
    if request.user.is_authenticated():
        return index(request)
    else:
        if 'username' and 'firstName'and 'lastName' and 'password' and 'email' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['firstName']
            last_name = request.POST['lastName']
            email = request.POST['email']

            try:
                User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                messages.success(request, "Account created successfully! Please login.")
                return index(request)

            except IntegrityError:
                messages.error(request, "That username has been taken! Try again.")
                return HttpResponseRedirect(reverse('planda:create_account'))

        else:
            return render(request, 'planda/create_account.html')