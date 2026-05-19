from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import CustomUserCreationForm


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

