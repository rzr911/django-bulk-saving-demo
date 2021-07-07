from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from icecream.api.viewsets import IceCreamViewset

from django_bulk_saving_benchmark.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("icecreams", IceCreamViewset)


app_name = "api"
urlpatterns = router.urls
