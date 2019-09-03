from django.conf import settings
    
import datetime

from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER



class AppConfig(DjangoAppConfig):
    name = 'td_export'
    today_date = datetime.datetime.now().strftime('%Y%m%d')
    export_date =  '/documents/td_export_' + today_date
    maternal_path = settings.MEDIA_ROOT + export_date + '/maternal/'
    infant_path = settings.MEDIA_ROOT + export_date + '/infant/'
    non_crf_path = settings.MEDIA_ROOT + export_date + '/non_crf/'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'TD Export'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = '99'
