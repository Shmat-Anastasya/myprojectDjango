from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserEditForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()          # создаём пользователя
            login(request, user)        # автоматически логиним
            return redirect('profile')  # отправляем в личный кабинет
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})

