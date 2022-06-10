  
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,  JsonResponse
from .forms import UserRegisterForm
# from Poll_app.models import Poll, Quiz
from requests import request


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# @login_required
# def profile(request):
#     if request.method == 'POST':
#     #     if "delete_poll" in request.POST:
#     #         if len(Poll.objects.filter(quiz__isnull=True).filter(pk=request.POST["delete_poll"]).filter(author=request.user.id)) == 0:
#     #             return JsonResponse({"error": "Poll not found for user"}, status=400)
#     #         Poll.objects.filter(quiz__isnull=True).filter(pk=request.POST["delete_poll"]).filter(author=request.user.id).delete()
#     #         return JsonResponse({"Received": "Poll Deleted"}, status=200)
#     #     if "delete_quiz" in request.POST:
#     #         if len(Quiz.objects.filter(pk=request.POST["delete_quiz"]).filter(author=request.user.id)) == 0:
#     #             return JsonResponse({"error": "Quiz not found for user"}, status=400)
#     #         Quiz.objects.filter(pk=request.POST["delete_quiz"]).filter(author=request.user.id).delete()
#     #         return JsonResponse({"Received": "Quiz Deleted"}, status=200)
#     #     return JsonResponse({"error": "No request data sent"}, status=400)
#         return JsonResponse({"error": "Not allowed yet"}, status=400)

#     else:
#         # user_polls=Poll.objects.filter(quiz__isnull=True).filter(author=request.user.id)
#         # user_quizes=Quiz.objects.filter(author=request.user.id)
#         context={}
#         # context ['polls']=user_polls
#         # context ['quizes']=user_quizes

#         return render(request, 'users/profile.html',context)