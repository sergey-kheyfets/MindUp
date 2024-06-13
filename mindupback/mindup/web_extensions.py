from django.http import HttpResponse, FileResponse, SimpleCookie, \
    HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404

from . import jwt_for_cookie
from .models import Guest, Organization, Meeting, MeetingTag


def is_entry_url(url):
    return "/authorisation" in url or "/registration" in url


def get_from_address(url):
    if "?from=" in url:
        from_url = url[url.index("?from=") + 6:]
    else:
        from_url = ""
    return from_url


def my_decorator(is_user_required=False, rickroll=False):
    def extract_user_decorator(func):
        def result(request, *args, **kwargs):
            user = get_user_from_cookie(request)
            url = request.build_absolute_uri()
            if 'HTTP_REFERER' in request.META:
                prev_url = request.META['HTTP_REFERER']
            else:
                prev_url = ""
            request.from_url = get_from_address(url)
            request.prev_from_url = get_from_address(prev_url)

            is_entry = is_entry_url(url)
            if user is None and is_user_required:
                if not is_entry:
                    return HttpResponseRedirect(f"/mindup/authorisation?from={url}")
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
    decoded_result = jwt_for_cookie.decode(request.COOKIES['mindup_jwt'])
    if decoded_result is None or 'email' not in decoded_result:
        return None
    guest_email = decoded_result['email']
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
