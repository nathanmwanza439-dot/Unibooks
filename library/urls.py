from django.urls import include, path

urlpatterns = [
    path('', include('library.urls_student')),
]
