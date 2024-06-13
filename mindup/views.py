import datetime

from django.shortcuts import render
from django.http import HttpResponse, FileResponse, SimpleCookie, \
    HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404
from django.template import loader
from django.utils import timezone

from . import extensions, jwt_for_cookie
from .models import Guest, Organization, Meeting, MeetingTag

from django.core.files.storage import FileSystemStorage

from .web_extensions import my_decorator, get_user_from_cookie, set_user_to_cookie
from .rofls import Rofls


def show_cookie(request):
    return JsonResponse(request.COOKIES)


@my_decorator()
def me(request):
    return JsonResponse(get_user_from_cookie(request).to_dict())


@my_decorator()
def index(request):
    if request.user is not None:
        return HttpResponseRedirect("/mindup/meetings")
    return HttpResponseRedirect("/mindup/authorisation")


def login_post(request):
    print(request.POST)
    email = request.POST['email']
    password = request.POST['password']
    guests = list(Guest.objects.filter(email=email))
    if len(guests) == 0:
        return HttpResponse("account doesn't found")
    if not guests[0].check_password(password):
        return HttpResponse("incorrect password")
    guest = guests[0]
    response = HttpResponseRedirect("/mindup/groups")

    set_user_to_cookie(guest, response)

    return response


def register_post(request):
    user_name = request.POST['userName']
    sur_name = request.POST['sur_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST["password"]

    if len(Guest.objects.filter(email=email)) != 0:
        return HttpResponseBadRequest("аккаунт с таким email уже существует")

    new_guest = Guest(name=user_name, sur_name=sur_name, last_name=last_name, email=email,
                      password=extensions.get_password_hash(password), pub_date=timezone.now(),
                      origin_password=password)
    new_guest.save()
    response = HttpResponseRedirect("/mindup/authorisation")
    return response


@my_decorator()
def my_groups(request):
    return JsonResponse({'result':
                             [organization.to_dict() for organization in Organization.objects.filter(members=request.user.id)]})


@my_decorator()
def all_groups(request):
    return JsonResponse({'result': [organization.to_dict(request.user) for organization in Organization.objects.all()]})


@my_decorator()
def my_account(request):
    data = [get_user_from_cookie(request).to_dict()]
    return JsonResponse({'result': data})


@my_decorator()
def all_guests(request):
    data = [guest.to_dict() for guest in Guest.objects.all()]
    return JsonResponse({'result': data})


@my_decorator()
def all_tags(request):
    return JsonResponse({'result': [tag.to_dict() for tag in MeetingTag.objects.all()]})


@my_decorator()
def meeting_about(request, group_id, meeting_id):
    guest = request.user
    meeting = Meeting.objects.get(id=meeting_id)
    data = meeting.to_dict(guest)
    return JsonResponse({'result': data})


@my_decorator()
def meeting_members(request, group_id, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    data = [guest.to_dict() for guest in meeting.members.all()]
    return JsonResponse({'result': data})


@my_decorator()
def all_meetings(request):
    guest = request.user
    data = [meeting.to_dict(guest) for meeting in Meeting.objects.all()]
    data.sort(key=lambda x: x['event_time'])
    return JsonResponse({'result': data})


@my_decorator()
def my_meetings(request):
    guest =request.user
    return JsonResponse({'result':
                             [meeting.to_dict() for meeting in Meeting.objects.filter(members=guest)]})


@my_decorator()
def group_about(request, group_id):
    guest = request.user
    return JsonResponse({'result':  Organization.objects.get(id=group_id).to_dict(guest)})


@my_decorator()
def group_meetings(request, group_id):
    guest = request.user
    data = [meeting.to_dict(guest) for meeting in Meeting.objects.filter(organization_id=group_id)]
    return JsonResponse({'result': data})


@my_decorator()
def send_group(request):
    creator = request.user
    title = request.POST['title']
    description = request.POST['title']
    if 'image' in request.FILES:
        file = request.FILES['image']
        file_name = creator.name + "_" + extensions.generate_random_string(10) + "." + file.name.split('.')[-1]
        # file.name = file_name
        # print(file.__dict__)
        uploaded_file_url = "/mindup/groups_images/" + file_name
        file_path = "mindup/static/groups_images/" + file_name
        extensions.save_image_from_bytes(file_path, file.file)
    else:
        uploaded_file_url = '-'
    o = Organization(creator=creator, title=title, description=description, icon=uploaded_file_url)
    o.save()
    o.members.add(creator)
    o.save()
    return HttpResponseRedirect(f"/meetings.html?group={o.id}&title={o.title}")


@my_decorator()
def get_tag(tag_name):
    if tag_name[0] != '#':
        tag_name = '#' + tag_name
    aa = MeetingTag.objects.filter(title=tag_name)
    if len(aa) > 0:
        return aa[0]
    t = MeetingTag(title=tag_name)
    t.save()
    return t


@my_decorator()
def send_meeting(request):
    guest = request.user
    if 'organization_id' in request.POST and request.POST['organization_id'].isdigit():
        organization_id = int(request.POST['organization_id'])
    else:
        organization_id = 17
    organization = Organization.objects.get(id=organization_id)
    title = request.POST['name']
    description = request.POST['description']
    picture = request.POST['place']
    place_text = request.POST['place']
    place_link = request.POST['place']
    event_time = datetime.datetime.now().replace(
        hour=int(request.POST['time'].split(":")[0]),
        minute=int(request.POST['time'].split(":")[1]),
        year=int(request.POST['date'].split("-")[0]),
        month=int(request.POST['date'].split("-")[1]),
        day=int(request.POST['date'].split("-")[2]),
    )
    max_members_number = min(int(request.POST['max_members_number']), 9999999) \
        if 'max_members_number' in request.POST else 0
    is_max_members_number_limited = request.POST['is_max_members_number_limited'] \
        if 'is_max_members_number_limited' in request.POST else False
    tag_index = 1
    tags = []

    while 'tag' + str(tag_index) in request.POST:
        tags.append(request.POST['tag' + str(tag_index)])
        tag_index += 1
    tags_arr = []
    for tag in tags:
        tags_arr.append(get_tag(tag))
    if len(Meeting.objects.filter(organization=organization, title=title, description=description)) > 0:
        return HttpResponse('<h1><blink>возможно уже есть встреча с похожей тематикой в этой группе</blink></h1>'
                            + Rofls.open_window)
    d = Meeting(
        creator=guest,
        organization=organization,
        title=title,
        description=description,
        picture=picture,
        place_text=place_text,
        place_link=place_link,
        event_time=event_time,
        max_members_number=max_members_number,
        is_max_members_number_limited=is_max_members_number_limited
    )
    d.save()
    for tag in tags_arr:
        d.tags.add(tag)
    d.members.add(guest)
    d.save()
    return HttpResponseRedirect(f"/mindup/meetings.html?group={organization_id}&title={organization.title}")


@my_decorator()
def signup_meeting(request, group_id, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    meeting.members.add(request.user)
    meeting.save()
    return JsonResponse({'result': 'success'})


@my_decorator()
def unsignup_meeting(request, group_id, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    meeting.members.remove(request.user)
    meeting.save()
    return JsonResponse({'result': 'success'})
