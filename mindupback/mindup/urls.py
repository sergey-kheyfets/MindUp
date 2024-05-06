from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("authorization", views.authorization, name="authorization"),
    path("styles.css", views.styles_css, name="styles_css"),
    path("authorization.css", views.authorization_css, name="authorization_css"),
    path("authorization.css", views.groups_css, name="groups_css"),
    path("pngwing.com.png", views.img)
]