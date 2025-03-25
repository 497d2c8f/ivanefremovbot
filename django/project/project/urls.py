from django.contrib import admin
from django.urls import path, include
from bot import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tasks', views.TaskModelViewSet, basename='tasks')
router.register(r'tags', views.TagModelViewSet, basename='tags')


urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include(router.urls))
]
