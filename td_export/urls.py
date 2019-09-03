from django.urls.conf import path

from .admin_site import td_export_admin
from .views import HomeView, ListBoardView

from edc_dashboard import UrlConfig

from .patterns import export_identifier

app_name = 'td_export'

urlpatterns = [
    path('admin/', td_export_admin.urls),
    path('', HomeView.as_view(), name='home_url'),
]


export_listboard_url_config = UrlConfig(
    url_name='export_listboard_url',
    view_class=ListBoardView,
    label='export_listboard',
    identifier_label='export_identifier',
    identifier_pattern=export_identifier)


urlpatterns += export_listboard_url_config.listboard_urls
