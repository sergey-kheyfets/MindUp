from django.urls import path, re_path

from . import views, file_views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_post, name="login"),
    path("register", views.register_post, name="register"),

    path("api/login", views.login_post, name="login"),
    path("api/register", views.register_post, name="register"),
    path("api/send_meeting", views.send_meeting, name="send_meeting"),
    path("api/send_group", views.send_group, name="send_group"),

    path("api/me", views.me),
    path("api/my_groups", views.my_groups),
    path("api/all_groups", views.all_groups),
    path("api/my_account", views.my_account),
    path('api/all_guests', views.all_guests),
    path('api/all_meetings', views.all_meetings),
    path('api/my_meetings', views.my_meetings),
    path('api/all_tags', views.all_tags),

    path("api/group/<int:group_id>", views.group_about),
    path("api/group/<int:group_id>/meetings", views.group_meetings),
    path("api/group/<int:group_id>/meeting/<int:meeting_id>", views.meeting_about),
    path("api/group/<int:group_id>/meeting/<int:meeting_id>/guests", views.meeting_members),

    path('api/group/<int:group_id>/<int:meeting_id>/signup', views.signup_meeting),
    path('api/group/<int:group_id>/<int:meeting_id>/unsignup', views.unsignup_meeting),


    re_path(r"^(?P<file_name>[a-zA-Z_0-9]+).(?P<file_extension>css|js)", file_views.get_static, name="get_static"),
    re_path(r"^(?P<folder_name>([a-zA-Z_0-9]+)_styles)/(?P<file_name>[a-zA-Z_0-9]+).(?P<file_extension>css|js)",
            file_views.get_folder_static, name="get_folder_static"), # not used


    re_path(r"^(?P<file_name>[a-zA-Z_0-9.]+).(?P<file_extension>png|jpg|jpeg|svg)", file_views.get_img, name="get_img"),
    re_path(r"^(?P<folder_name>[a-zA-Z_0-9]+_images)/(?P<file_name>[a-zA-Z_0-9]+).(?P<file_extension>png|jpg|jpeg|svg)",
            file_views.get_folder_img, name="get_folder_img"),

    re_path(r"^(?P<file_name>[a-zA-Z_0-9]+)(.html)?", file_views.get_html_template, name="get_html_template"),
    re_path(r"^(?P<folder_name>[a-zA-Z_0-9]+_html)/(?P<file_name>[a-zA-Z_0-9]+)(.html)?",
            file_views.get_folder_html_template, name="get_html_template"), # not used
]