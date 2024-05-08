from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("authorization", views.authorization_template, name="authorization"),
    path("login", views.login_post, name="login"),
    path("groups", views.groups_template, name="groups"),

    path("api/my_groups", views.my_groups),
    path("api/all_groups", views.all_groups),
    path("api/my_account", views.my_account),
    path('api/all_guests', views.all_guests),
    path('api/all_meetings', views.all_meetings),

    path("api/group/<int:group_id>/meetings", views.groups_meetings),

    re_path(r"^(?P<file_name>[a-zA-Z]+).css", views.get_css, name="get_css"),
    re_path(r"^(?P<folder_name>([a-zA-Z]+)_styles)/(?P<file_name>[a-zA-Z]+).css",
            views.get_folder_css, name="get_folder_css"),

    re_path(r"^(?P<file_name>[a-zA-Z]+).html", views.get_html_template, name="get_html_template"),
    re_path(r"^(?P<folder_name>[a-zA-Z]+_html)/(?P<file_name>[a-zA-Z]+).html",
            views.get_folder_html_template, name="get_html_template"),

    re_path(r"^(?P<file_name>[a-zA-Z_]+).(?P<file_extension>png|jpg|jpeg|svg)", views.get_img, name="get_img"),
    re_path(r"^(?P<folder_name>[a-zA-Z]+_images)/(?P<file_name>[a-zA-Z_]+).(?P<file_extension>png|jpg|jpeg|svg)",
            views.get_folder_img, name="get_folder_img"),

    path("pngwing.com.png", views.img)
]