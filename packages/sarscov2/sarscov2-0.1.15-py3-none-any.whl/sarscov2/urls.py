from django.urls.conf import path
from django.views.generic import RedirectView

from .admin_site import sarscov2_admin

app_name = "sarscov2"

urlpatterns = [
    path("admin/", sarscov2_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
