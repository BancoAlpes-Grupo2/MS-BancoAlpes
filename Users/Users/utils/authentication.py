from django.http import JsonResponse
from functools import wraps
import jwt

def jwt_required(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        token = request.COOKIES.get('authToken')
        if not token:
            return JsonResponse({'message': 'Authorization token is missing'}, status=401)
        try:
            payload = jwt.decode(token, '3=tduj+4yyua6k&qx@g(xbyx69w6t_p=o$x$fcb8dw$-_g$dws', algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid token'}, status=401)

        return f(request, *args, **kwargs)
    return decorated