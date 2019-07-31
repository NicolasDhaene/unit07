from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"sign_in", views.sign_in, name="sign_in"),
    url(r"sign_up", views.sign_up, name="sign_up"),
    url(r"sign_out", views.sign_out, name="sign_out"),
    url(r"(?P<pk>\d+)/$", views.view_profile, name="view_profile"),
    url(r"(?P<pk>\d+)/edit", views.edit_profile, name="edit_profile"),
    url(r"(?P<pk>\d+)/change_password", views.change_password, name="change_password"),
]
