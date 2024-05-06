from django.urls import path

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

    path("styles.css", views.styles_css, name="styles_css"),
    path("authorization.css", views.authorization_css, name="authorization_css"),
    path("authorization.css", views.groups_css, name="groups_css"),
    path("pngwing.com.png", views.img)
]