from django.http import HttpResponse, FileResponse, SimpleCookie,\
    HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
#from PIL import Image
#from io import BytesIO
import os


def get_html_template(request, file_name):
    file_path = f"mindup/templates/{file_name}.html"
    if not os.path.isfile(file_path):
        return HttpResponseNotFound(f"file {file_path} not found")

    return HttpResponse(open(file_path, encoding="utf8"))


def get_folder_html_template(request, folder_name, file_name):
    file_path = f"mindup/templates/{folder_name}/{file_name}.html"
    if not os.path.isfile(file_path):
        return HttpResponseNotFound(f"file {file_path} not found")

    return HttpResponse(open(file_path, encoding="utf8"))


def get_static(request, file_name, file_extension):
    content_type = "javascript" if file_extension == "js" else file_extension
    file_path = f"mindup/static/{file_name}.{file_extension}"
    if not os.path.isfile(file_path):
        return HttpResponseNotFound(f"file {file_path} not found")

    return HttpResponse(open(file_path, encoding="utf8"), content_type=f"text/{content_type}")


def get_folder_static(request, folder_name, file_name, file_extension):
    file_path = f"mindup/static/{folder_name}/{file_name}.{file_extension}"
    content_type = "javascript" if file_extension == "js" else file_extension
    if not os.path.isfile(file_path):
        return HttpResponseNotFound(f"file {file_path} not found")
    return HttpResponse(open(file_path, encoding="utf8"), content_type=f"text/{content_type}")


def get_img(request, file_name, file_extension):
    image_path = f"mindup/static/{file_name}.{file_extension}"
    if not os.path.isfile(image_path):
        return HttpResponseNotFound(f"file {image_path} not found")
    if file_extension == 'svg':
        return HttpResponse(open(image_path, encoding="utf8"), content_type="image/svg+xml")

    return img_from_path(image_path, file_extension)


def get_folder_img(request, folder_name, file_name, file_extension):
    image_path = f"mindup/static/{folder_name}/{file_name}.{file_extension}"
    if not os.path.isfile(image_path):
        return HttpResponseNotFound(f"file {image_path} not found")
    if file_extension == 'svg':
        return HttpResponse(open(image_path, encoding="utf8"), content_type="image/svg+xml")

    return img_from_path(image_path, file_extension)


def img_from_path2(image_path, file_extension):
    pass
    # file_extension == "jpg":
    #    file_extension = "jpeg"
    #image = Image.open(image_path)
    #image = Image.open(image_path)
    # Image._show(image)
    # Создаем байтовый объект для хранения изображения
    #image_byte_array = BytesIO()
    #image.save(image_byte_array, format=file_extension.upper())

    # Возвращаем ответ с содержимым изображения
    #return HttpResponse(image_byte_array.getvalue(), content_type=f"image/{file_extension.lower()}")


def img_from_path(image_path, file_extension):
    if file_extension == "jpg":
        file_extension = "jpeg"

    image = open(image_path, 'rb')

    return HttpResponse(image, content_type=f"image/{file_extension.lower()}")
