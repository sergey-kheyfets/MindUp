from django.http import HttpResponse, FileResponse, SimpleCookie, \
    HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404

from . import extensions, jwt_for_cookie
from .models import Guest, Organization, Meeting, MeetingTag


def my_decorator(is_user_required=False, rickroll=False):
    def extract_user_decorator(func):
        def result(request, *args, **kwargs):
            user = get_user_from_cookie(request)
            if user is None and is_user_required:
                return HttpResponseRedirect("/mindup/login")
            elif user is not None and user.last_name == "zv" and rickroll:
                return HttpResponseRedirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            request.user = user
            return func(request, *args, **kwargs)
        return result
    return extract_user_decorator


def redirect_decorator(func):
    def dick(request, *args, **kwargs):
        user = get_user_from_cookie(request)
        if user is None:
            return HttpResponseRedirect("/mindup/login")
        return func(request, *args, **kwargs)
    return dick


def get_user_from_cookie_old(request):
    if 'mindup_email' not in request.COOKIES:
        return None
    users = Guest.objects.filter(email=request.COOKIES['mindup_email'])
    if len(users) == 0:
        return None
    user = users[0]
    if user.check_password(request.COOKIES['mindup_password']):
        return user


def get_user_from_cookie(request):
    if 'mindup_jwt' not in request.COOKIES:
        return None
    guest_email = jwt_for_cookie.decode(request.COOKIES['mindup_jwt'])['email']
    if guest_email is None:
        return None

    users = Guest.objects.filter(email=guest_email)
    if len(users) == 0:
        return None
    return users[0]


def set_user_to_cookie(guest, response):
    #cookie = SimpleCookie()
    #print(email, password)
    #cookie['mindup_email'] = email
    #cookie['mindup_email']['max-age'] = 3600
    #cookie['mindup_password'] = password
    #cookie['mindup_password']['max-age'] = 3600

    # response['Set-Cookie'] = cookie.output(header='').replace('\n', '').replace('\r', '')
    # response.set_cookie(key='mindup_email', value=guest.email, max_age=3600)
    # response.set_cookie(key='mindup_password', value=guest.origin_password, max_age=3600)
    response.set_cookie(key='mindup_jwt', value=jwt_for_cookie.encode({"email": guest.email}), max_age=3600)
