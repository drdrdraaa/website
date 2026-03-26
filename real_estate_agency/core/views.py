from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Realtor, Property, CallRequest, Payment

def home(request):
    realtors = Realtor.objects.filter(is_active=True).prefetch_related('properties')
    context = {
        'realtors': realtors,
    }
    return render(request, 'home.html', context)

def realtor_detail(request, realtor_id):
    realtor = get_object_or_404(Realtor, id=realtor_id, is_active=True)
    properties = Property.objects.filter(realtor=realtor, is_available=True)
    context = {
        'realtor': realtor,
        'properties': properties,
    }
    return render(request, 'realtor_detail.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')

@csrf_exempt
@require_POST
def call_request_api(request):
    try:
        property_id = request.POST.get('property_id')
        realtor_id = request.POST.get('realtor_id')
        client_name = request.POST.get('client_name')
        client_phone = request.POST.get('client_phone')
        client_email = request.POST.get('client_email', '')
        message = request.POST.get('message', '')
        
        # Проверка капчи (в реальном приложении здесь будет проверка reCAPTCHA)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response:
            return JsonResponse({'success': False, 'message': 'Пройдите проверку капчи'})
        
        # Создание запроса звонка
        call_request = CallRequest.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            client_email=client_email,
            realtor_id=realtor_id,
            property_id=property_id if property_id else None,
            message=message
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Запрос успешно отправлен',
            'request_id': call_request.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@require_POST
def payment_api(request):
    try:
        property_id = request.POST.get('property_id')
        realtor_id = request.POST.get('realtor_id')
        client_name = request.POST.get('client_name')
        client_phone = request.POST.get('client_phone')
        client_email = request.POST.get('client_email')
        
        # Проверка капчи
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response:
            return JsonResponse({'success': False, 'message': 'Пройдите проверку капчи'})
        
        # Получение риелтора для расчета комиссии
        realtor = get_object_or_404(Realtor, id=realtor_id)
        
        # Создание запроса звонка
        call_request = CallRequest.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            client_email=client_email,
            realtor=realtor,
            property_id=property_id if property_id else None,
            status='confirmed'
        )
        
        # Расчет комиссии (тестовый - 1000 рублей)
        commission_amount = 1000.00
        
        # Создание платежа
        payment = Payment.objects.create(
            call_request=call_request,
            amount=commission_amount,
            status='completed',
            transaction_id=f'test_{call_request.id}_{int(call_request.created_at.timestamp())}'
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Оплата успешно обработана',
            'payment_id': payment.id,
            'amount': commission_amount
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
