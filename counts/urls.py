from django.urls import path

from counts.views import counts

urlpatterns = [
    path('', counts, name='counts'),
]