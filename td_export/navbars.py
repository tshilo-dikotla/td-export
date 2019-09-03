from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'td_export' else False

td_export = Navbar(name='td_export')

td_export.append_item(
    NavbarItem(
        name='export_data',
        title='Export Data',
        label='TD Export Data',
        fa_icon='fa fa-file-export',
        url_name=settings.DASHBOARD_URL_NAMES[
            'export_listboard_url'],
        no_url_namespace=no_url_namespace))


site_navbars.register(td_export)
