from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from utils.jwt_helper import decode_jwt
from .models import CustomUser

def protected_view(request):
    token = request.COOKIES.get('jwt')

    
    if not token:
        return redirect('/apps/login/')  

    try:
        
        payload = decode_jwt(token)
        user_id = payload.get('user_id')

        user = CustomUser.objects.get(id=user_id)

        return JsonResponse({
            'message': f'Welcome {user.name}',
            'user': {
                'name': user.name,
                'phone': user.phone
            }
        })

    except Exception as e:
        return redirect('/apps/login/')
