from django.urls import path

from .views import (
    edit_view,
    index,
    entry_view,
    create_view,
    random_view,
    search_view,
    delete_view,
)

app_name = 'encyclopedia'
urlpatterns = [
    path("", index, name="index"),
    path('wiki/random/', random_view, name='random'),
    path('wiki/create/', create_view, name='create'),
    path('wiki/search/', search_view, name='search'),
    path('wiki/<str:title>/', entry_view, name='entry'),
    path('wiki/<str:title>/edit/', edit_view, name='edit'),
    path('wiki/<str:title>/delete/', delete_view, name='delete'),
]
