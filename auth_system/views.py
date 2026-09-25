from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


def _safe_next(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Акаунт створено. Тепер можна увійти.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'auth_system/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(_safe_next(request) or 'home')
    else:
        form = AuthenticationForm()

    return render(
        request,
        'auth_system/login.html',
        {
            'form': form,
            'next': request.POST.get('next') or request.GET.get('next', ''),
        },
    )


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')
