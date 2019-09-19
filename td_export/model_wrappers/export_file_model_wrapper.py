from django.conf import settings
from edc_model_wrapper import ModelWrapper


class ExportFileModelWrapper(ModelWrapper):

    model = 'td_export.exportfile'
    next_url_attrs = ['export_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'export_listboard_url')


    @property
    def file_url(self):
        """Return the file url.
        """
        return self.object.document.url

    @property
    def files_generation_time(self):
        """return file generation time in minutes
        """
        return round(float(self.object.downnload_time)/60.0, 2)