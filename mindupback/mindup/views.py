from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template import loader
from PIL import Image
from io import BytesIO
from django.http import FileResponse

from .models import Guest, Organization, Meeting


def index(request):
    return HttpResponse(open("mindup/templates/index.html", encoding="utf8"))


def authorization(request):
    return HttpResponse(open("mindup/templates/authorization.html", encoding="utf8"))


def styles_css(request):
    return HttpResponse(open("mindup/static/styles.css", encoding="utf8"), content_type="text/css")


def authorization_css(request):
    return HttpResponse(open("mindup/static/authorization.css", encoding="utf8"), content_type="text/css")


def groups_css(request):
    return HttpResponse(open("mindup/static/groups.css", encoding="utf8"), content_type="text/css")


def img(request):
    image_path = "mindup/static/pngwing.com.png"  # Путь к вашей картинке
    image = Image.open(image_path)
    #Image._show(image)
    # Создаем байтовый объект для хранения изображения
    image_byte_array = BytesIO()
    image.save(image_byte_array, format='PNG')

    # Возвращаем ответ с содержимым изображения
    print(image_byte_array.getvalue())
    return HttpResponse(image_byte_array.getvalue(), content_type='image/png')
