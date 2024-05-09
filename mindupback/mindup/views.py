from django.shortcuts import render
from django.http import HttpResponse, FileResponse, SimpleCookie, HttpResponseRedirect, JsonResponse
from django.template import loader
from PIL import Image
from io import BytesIO

from .models import Guest, Organization, Meeting


def get_user_from_cookie(request):
    user = Guest.objects.filter(email=request.COOKIES['mindup_email'])
    return user[0]


def index(request):
    return HttpResponse(open("mindup/templates/index.html", encoding="utf8"))


def login_post(request):
    email = request.POST['email']
    password = request.POST['password']
    dick = list(Guest.objects.filter(email=email))
    if len(dick) == 0:
        return HttpResponse("account doesn't found")
    if dick[0].password != password:
        return HttpResponse("incorrect password")

    cookie = SimpleCookie()
    cookie['mindup_email'] = email
    cookie['mindup_email']['max-age'] = 3600

    response = HttpResponseRedirect("/mindup/groups")
    response['Set-Cookie'] = cookie.output(header='')
    return response


def my_groups(request):
    me = Guest.objects.get(id=1)
    return JsonResponse({'result':
        [organization.to_dict() for organization in Organization.objects.filter(members=me)]})


def all_groups(request):
    return JsonResponse({'result': [organization.to_dict() for organization in Organization.objects.all()]})


def my_account(request):
    data = [get_user_from_cookie(request).to_dict()]
    return JsonResponse({'result': data})


def all_guests(request):
    data = [guest.to_dict() for guest in Guest.objects.all()]
    return JsonResponse({'result': data})


def all_meetings(request):
    data = [meeting.to_dict() for meeting in Meeting.objects.all()]
    return JsonResponse({'result': data})


def groups_meetings(request, group_id):
    data = [meeting.to_dict() for meeting in Meeting.objects.filter(organization_id=group_id)]
    return JsonResponse({'result': data})


def get_html_template(request, file_name):
    return HttpResponse(open(f"mindup/templates/{file_name}.html", encoding="utf8"))


def get_folder_html_template(request, folder_name, file_name):
    return HttpResponse(open(f"mindup/templates/{folder_name}/{file_name}.html", encoding="utf8"))


def get_static(request, file_name, file_extension):
    if file_extension == "js":
        content_type = "javascript"
    else:
        content_type = file_extension
    return HttpResponse(open(f"mindup/static/{file_name}.{file_extension}", encoding="utf8"),
                        content_type=f"text/{content_type}")


def get_folder_static(request, folder_name, file_name, file_extension):
    if file_extension == "js":
        content_type = "javascript"
    else:
        content_type = file_extension
    return HttpResponse(open(f"mindup/static/{folder_name}/{file_name}.{file_extension}", encoding="utf8"),
                        content_type=f"text/{content_type}")


def get_img(request, file_name, file_extension):
    image_path = f"mindup/static/{file_name}.{file_extension}"  # Путь к вашей картинке
    return img_from_path(image_path, file_extension)


def get_folder_img(request, folder_name, file_name, file_extension):
    if file_extension == 'svg':
        return HttpResponse(open(f"mindup/static/{folder_name}/{file_name}.svg", encoding="utf8"),
                            content_type="image/svg+xml")

    image_path = f"mindup/static/{folder_name}/{file_name}.{file_extension}"  # Путь к вашей картинке
    return img_from_path(image_path, file_extension)


def img_from_path(image_path, file_extension):
    image = Image.open(image_path)
    # Image._show(image)
    # Создаем байтовый объект для хранения изображения
    image_byte_array = BytesIO()
    image.save(image_byte_array, format=file_extension.upper())

    # Возвращаем ответ с содержимым изображения
    return HttpResponse(image_byte_array.getvalue(), content_type='image/png')
