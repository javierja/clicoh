from rest_framework.routers import DefaultRouter
from users.api.viewsets import UserViewSet


router=DefaultRouter()

router.register(r'', UserViewSet, basename='users')

urlpatterns=router.urls