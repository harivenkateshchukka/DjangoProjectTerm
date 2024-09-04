import socket

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import UserDetailsForm, BiometricDetailsForm, CustomLoginForm, QuestionForm, SubmissionForm, GradeForm
from .models import UserDetails, BiometricDetails, Question, Submission, Grade, Active
from django.contrib.auth.models import User

@login_required
def admin_base(request):
    return render(request, 'admin_base.html')

@login_required
def user_base(request):
    return render(request, 'user_base.html')

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)

                    if user.is_staff:
                        return redirect('admin_base')
                    else:
                        if user:
                            ur = User.objects.get(username=email)
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            try:
                                s.connect(("8.8.8.8", 80))
                                user_ip = s.getsockname()[0]
                            except socket.error:
                                user_ip = None
                            finally:
                                s.close()
                            Active.objects.create(username=ur, ipaddress=user_ip)
                            obj1 = Active.objects.filter(Q(username=ur) & Q(ipaddress=user_ip)).count()
                            obj2 = Active.objects.filter(Q(username=ur)).count()
                            max_value = max(obj1, obj2)
                            print(user)
                            if max_value < 10:
                                request.session['custom_data'] = ur.email
                                return render(request, "user_base.html",{"custom_data": ur.email})
                            else:
                                return render(request, "home2.html",{"custom_data": ur.email})
                        return redirect('submit_answer')
                else:
                    form.add_error(None, "Invalid email or password.")
            except User.DoesNotExist:
                form.add_error(None, "Invalid email or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserDetailsForm(request.POST)
        bio_form = BiometricDetailsForm(request.POST, request.FILES)

        if user_form.is_valid() and bio_form.is_valid():
            email = user_form.cleaned_data.get('email')
            first_name = user_form.cleaned_data.get('first_name')
            last_name = user_form.cleaned_data.get('last_name')
            password = user_form.cleaned_data.get('password')

            # Create a new User instance
            user = User.objects.create_user(username=email, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password) # Set the password properly
            user.save()

            # Create the UserDetails instance
            user_details = UserDetails.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            # Create the BiometricDetails instance
            bio = bio_form.save(commit=False)
            bio.user = user_details
            bio.save()

            return redirect('success')
    else:
        user_form = UserDetailsForm()
        bio_form = BiometricDetailsForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'bio_form': bio_form})

def home(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'registration/success.html')

# Admin Views
@login_required
def upload_question(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()

    return render(request, 'registration/upload_question.html', {'form': form})

@login_required
def view_submissions(request):
    if not request.user.is_staff:
        return redirect('home')
    submissions = Submission.objects.all()
    return render(request, 'registration/view_submissions.html', {'submissions': submissions})

@login_required
def grade_submission(request, submission_id):
    if not request.user.is_staff:
        return redirect('home')
    submission = get_object_or_404(Submission, id=submission_id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.submission = submission
            grade.save()
            return redirect('view_submissions')
    else:
        form = GradeForm()

    return render(request, 'registration/grade_submission.html', {'form': form, 'submission': submission})

# User Views
@login_required
def question_list(request):
    if request.user.is_staff:
        return redirect('home')
    questions = Question.objects.all()
    return render(request, 'registration/question_list.html', {'questions': questions})

@login_required
def submit_answer(request):
    if request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = UserDetails.objects.get(user=request.user)
            submission.save()
            return redirect('view_grades')
    else:
        form = SubmissionForm()

    return render(request, 'registration/submit_answer.html', {'form': form})

@login_required
def view_grades(request):
    if request.user.is_staff:
        return redirect('home')
    user = UserDetails.objects.get(user=request.user)
    submissions = Submission.objects.filter(user=user)
    return render(request, 'registration/view_grades.html', {'submissions': submissions})

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def logged_out_view(request):
    return render(request, 'user_base.html')  # Or use a dedicated template for logout

