from django.shortcuts import render
from django.http import HttpResponse, FileResponse, SimpleCookie, \
    HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404
from django.template import loader
from django.utils import timezone

from . import extensions
from .models import Guest, Organization, Meeting, MeetingTag


def get_user_from_cookie(request):
    if 'mindup_email' not in request.COOKIES:
        return None
    users = Guest.objects.filter(email=request.COOKIES['mindup_email'])
    if len(users) == 0:
        return None
    user = users[0]
    if user.check_password(request.COOKIES['mindup_password']):
        return user


def me(request):
    return JsonResponse(get_user_from_cookie(request).to_dict())


def index(request):
    return HttpResponse(open("mindup/templates/index.html", encoding="utf8"))


def login_post(request):
    email = request.POST['email']
    password = request.POST['password']
    dick = list(Guest.objects.filter(email=email))
    if len(dick) == 0:
        return HttpResponse("account doesn't found")
    if not dick[0].check_password(password):
        return HttpResponse("incorrect password")

    cookie = SimpleCookie()
    print(email, password)
    cookie['mindup_email'] = email
    cookie['mindup_email']['max-age'] = 3600
    cookie['mindup_password'] = password
    cookie['mindup_password']['max-age'] = 3600

    response = HttpResponseRedirect("/mindup/groups")
    # response['Set-Cookie'] = cookie.output(header='').replace('\n', '').replace('\r', '')
    response.set_cookie(key='mindup_email', value=email, max_age=3600)
    response.set_cookie(key='mindup_password', value=password, max_age=3600)
    return response


def register_post(request):
    user_name = request.POST['userName']
    email = request.POST['email']
    password = request.POST["password"]
    if len(Guest.objects.filter(email=email)) != 0:
        return HttpResponseBadRequest("аккаунт с таким email уже существует")

    new_guest = Guest(name=user_name, email=email,
                      password=extensions.get_password_hash(password), pub_date=timezone.now())
    new_guest.save()
    response = HttpResponseRedirect("/mindup/authorisation")
    return response


def my_groups(request):
    me = get_user_from_cookie(request)
    return JsonResponse({'result':
                             [organization.to_dict() for organization in Organization.objects.filter(members=me.id)]})


def all_groups(request):
    me = get_user_from_cookie(request)
    print(me)
    return JsonResponse({'result': [organization.to_dict(me) for organization in Organization.objects.all()]})


def my_account(request):
    data = [get_user_from_cookie(request).to_dict()]
    return JsonResponse({'result': data})


def all_guests(request):
    data = [guest.to_dict() for guest in Guest.objects.all()]
    return JsonResponse({'result': data})


def meeting_members(request, group_id, meeting_id):
    data = [guest.to_dict() for guest in Guest.objects.all()]
    return JsonResponse({'result': data})


def all_meetings(request):
    guest = get_user_from_cookie(request)
    data = [meeting.to_dict(guest) for meeting in Meeting.objects.all()]
    return JsonResponse({'result': data})


def my_meetings(request):
    guest = get_user_from_cookie(request)
    return JsonResponse({'result':
                             [meeting.to_dict() for meeting in Meeting.objects.filter(members=guest)]})


def groups_meetings(request, group_id):
    guest = get_user_from_cookie(request)
    data = [meeting.to_dict(guest) for meeting in Meeting.objects.filter(organization_id=group_id)]
    return JsonResponse({'result': data})


def get_tag(tag_name):
    aa = MeetingTag.objects.filter(title=tag_name)
    if len(aa) > 0:
        return aa[0]
    if tag_name[0] != '#':
        tag_name = '#' + tag_name
    t = MeetingTag(name=tag_name)
    t.save()
    return t


def send_meeting(request, organization_id):
    guest = get_user_from_cookie(request)
    title = request.POST['title']
    description = request.POST['description']
    picture = request.POST['picture']
    place_text = request.POST['place_text']
    place_link = request.POST['place_link']
    event_time = request.POST['event_time']
    max_members_number = request.POST['max_members_number']
    tags = request.POST['tags']
    tags_arr = []
    for tag in tags:
        tags_arr.append(get_tag(tag))
    d = Meeting(
        creator=guest,
        organization=organization_id,
        title=title,
        description=description,
        picture=picture,
        place_text=place_text,
        place_link=place_link,
        event_time=event_time,
        max_members_number=max_members_number
    )
    d.save()
    return HttpResponseRedirect(f"mindup/group/{organization_id}")


def signup_meeting(request, group_id, meeting_id):
    me = get_user_from_cookie(request)
    meeting = Meeting.objects.get(id=meeting_id)
    meeting.members.add(me)
    meeting.save()
    return JsonResponse({'result': 'success'})


def unsignup_meeting(request, group_id, meeting_id):
    me = get_user_from_cookie(request)
    meeting = Meeting.objects.get(id=meeting_id)
    meeting.members.remove(me)
    meeting.save()
    return JsonResponse({'result': 'success'})
