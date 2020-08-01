from django.core.exceptions import ValidationError

from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.core.mail import EmailMessage

from .forms import DonateForm
from .models import Donator

# Create your views here.
from django.http import HttpResponse


def index(request):
    context = {}
    return render(request, 'core/index.html', context)


def profile_check(user):

    print(user.donator)
    print(user.donator.location)
    print(user.donator.birth_date)
    #print(user.donator.full_clean())
    try:
        user.donator.full_clean()
    except ValidationError as e:
        return False
    return True

@user_passes_test(profile_check, login_url='/profile')
def results(request):
    context = {'result': 'Joe Biden'+request.user.donator.location}
    return render(request, 'core/results.html', context)


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        # user.donator.bio = form.cleaned_data.get('bio')
        # user.donator.birth_date = form.cleaned_data.get('birth_date')
        user.donator.first_name = form.cleaned_data.get('first_name')
        user.donator.last_name = form.cleaned_data.get('last_name')
        user.donator.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':

        form = DonateForm(request.POST, instance=request.user.donator)
        if form.is_valid():
            user = request.user

            user.donator = form.save()
            # user.donator.save()

            # user.donator.bio = form.cleaned_data.get('bio')
            # user.donator.birth_date = form.cleaned_data.get('birth_date')
            # user.donator.save()
            #
            # if request.method == 'POST':
            #     user_form = UserCreationForm(request.POST)
            #     donate_form = DonateForm(request.POST)
            #     if user_form.is_valid() and donate_form.is_valid():
            #         user = user_form.save()
            #         for field in profile_form.changed_data:
            #             setattr(user.profile, field, profile_form.cleaned_data.get(field))
            #         user.profile.save()
            # if request.method == 'POST':
            # # create a form instance and populate it with data from the request:
            #     form = DonateForm(request.POST)
            #     # check whether it's valid:
            #     if form.is_valid():
            #         # process the data in form.cleaned_data as required
            #
            #         donation = form.save()
            #         donation.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/results')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = DonateForm()

    context = {'form': form}
    return render(request, 'core/profile.html', context)

#
# def success(request):
#     context = {}
#     done = False
#     while not done:
#         toFill = Request.objects.all().order_by('time').first()
#
#         if not toFill:
#             done = True
#         else:
#             message = toFill.name + " has requested " + str(toFill.tickets) + (" ticket" if toFill.tickets==1 else " tickets")+". The donations are:\n\n"
#             donors = [Donation.objects.filter(tickets__gte=toFill.tickets).order_by('tickets').first()]
#             if not donors[0]:
#                 donors = []
#                 potentials = Donation.objects.all().order_by('-tickets')
#                 left = toFill.tickets
#
#                 finished = False
#                 count = 0
#                 while count < len(potentials) and not finished:
#                     if left - potentials[count].tickets <= 0:
#                         potentials[count].tickets -= left
#                         message+=potentials[count].name+": "+str(left)+(" ticket" if toFill.tickets==1 else " tickets")
#                         left = 0
#                         finished = True
#                     else:
#                         left -= potentials[count].tickets
#                         message += potentials[count].name + ": " + str(potentials[count].tickets) +(" ticket\n" if toFill.tickets==1 else " tickets\n")
#                         potentials[count].tickets = 0
#                     donors.append(potentials[count])
#                     count += 1
#                 if left != 0:  # cant fill any more
#                     done = True
#
#             else:
#                 donors[0].tickets -= toFill.tickets
#                 message+=donors[0].name+": "+str(toFill.tickets)+(" ticket" if toFill.tickets==1 else " tickets")
#
#             if not done:
#                 emails = [toFill.email]
#
#                 for donor in donors:
#                     emails.append(donor.email)
#                     donor.save()
#                     if donor.tickets == 0:
#                         donor.delete()
#                 closed=ClosedRequest(name=toFill.name,email=toFill.email,time=toFill.time,tickets=toFill.tickets)
#                 closed.save()
#                 toFill.delete()
#
#                 email = EmailMessage(
#                     'MBHS Graduation Ticket Swap',
#                     'This is an auto-generated email sent by graduation.mbhs.edu. You are receiving this email because you filled out a form either requesting or donating tickets for graduation. The other emails in the "To:" field are your matches; use them to organize your ticket exchange. Do not reply to this email address.\n\n'+message,
#                     'info@graduation.mbhs.edu',
#                     emails,
#                     ['mbhsgraduation@gmail.com']
#                 )
#                 email.send(fail_silently=False)
#
#
#     return render(request, 'core/success.html', context)
#
#
# def donate(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = DonateForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#
#             donation = form.save()
#             donation.save()
#
#             # redirect to a new URL:
#             return HttpResponseRedirect('/success')
#
#         # if a GET (or any other method) we'll create a blank form
#     else:
#         form = DonateForm()
#
#     context = {'form': form}
#     return render(request, 'core/donate.html', context)
#
#
# def request(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = RequestForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#
#             request = form.save(commit=False)
#             request.time = timezone.now()
#             total=0
#             for old in ClosedRequest.objects.all():
#                 if old.email == request.email:
#                     total+=old.tickets
#             if total>=4:
#                 return HttpResponseRedirect('/failed')
#
#             request.save()
#
#             # redirect to a new URL:
#             return HttpResponseRedirect('/success')
#
#         # if a GET (or any other method) we'll create a blank form
#     else:
#         form = RequestForm()
#
#     context = {'form': form}
#     return render(request, 'core/request.html', context)
