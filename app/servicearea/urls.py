"""
URL for the service area API
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from servicearea import views


router = DefaultRouter()
router.register('serviceareas-list', views.ServiceAreaViewSet)
router.register('servicearea-detail', views.ServiceAreaUpdateViewSet)


app_name = 'servicearea'

urlpatterns = [
    path('', include(router.urls)),
]
