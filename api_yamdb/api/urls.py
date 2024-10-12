from django.urls import include, path


urlpatterns = [
    path('v1/', include('api.reviews.urls')),
    path('v1/', include('api.users.urls')),
]
