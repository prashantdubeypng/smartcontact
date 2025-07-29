from django.http import JsonResponse
import json
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from utils.jwt_helper import generate_jwt
@csrf_exempt
# signup done
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')
            password = data.get('password')

            if not (name and phone and password):
                return JsonResponse({'error': 'All fields are required'}, status=400)
            if CustomUser.objects.filter(phone=phone).exists():
                return JsonResponse({'error': 'Phone already registered'}, status=400)
            
            hashed_password = make_password(password)
            user = CustomUser(name=name, phone=phone, password=hashed_password)
            user.save()
            token = generate_jwt({
                'user_id': user.id,
                'phone': user.phone
            })
            print(token)
            response = JsonResponse({
                'message': 'User registered successfully',
                'user': {
                    'name': user.name,
                    'phone': user.phone,
                }
            })
            response.set_cookie(
                key='jwt',
                value=token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600
            )
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone')
            password = data.get('password')

            if not phone or not password:
                return JsonResponse({'error': 'Phone and password are required'}, status=400)

            try:
                user = CustomUser.objects.get(phone=phone)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            if check_password(password, user.password):
                token = generate_jwt({
                'user_id': user.id,
                'phone': user.phone
            })
                response =  JsonResponse({
                    'message': 'Login successful',
                    'user': {
                        'name': user.name,
                        'phone': user.phone
                    }
                }, status=200)
                response.set_cookie(
                key='jwt',
                value=token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600
            )
                return response
            else:
                return JsonResponse({'error': 'Invalid password'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
# def save_contact(request):
#     try:
#         data = json.loads(request.body)
#         name = data.get('name')
#         phone_no = data.get('m_no')
#         relation = data.get('relation')
#         is_public = data.get('is_public')
#         action = data.get('action')