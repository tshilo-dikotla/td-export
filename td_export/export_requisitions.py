import pandas as pd, datetime, os

from django.apps import apps as django_apps


from .export_methods import ExportMethods
from .export_model_lists import exclude_fields


class ExportRequisitionData:
    """Export data.
    """

    def __init__(self, maternal_export_path=None, infant_export_path=None):
        self.maternal_export_path = maternal_export_path or django_apps.get_app_config('td_export').maternal_path
        self.infant_export_path = infant_export_path or django_apps.get_app_config('td_export').infant_path
        self.export_methods_cls = ExportMethods()

    def infant_requisitions(self):
        # Infant Requisiton Export

        crf_list = [
            'infantrequisition',
        ]
        karabo_panels = ['karabo_wb_pbmc_pl',
                         'karabo_pbmc_pl',
                         'infant_paxgene']

        for crf_name in crf_list:
            crf_cls = django_apps.get_model('td_infant', crf_name)
            objs = crf_cls.objects.all()
            count = 0
            crf_data = []
            for crf_obj in objs:
                data = self.export_methods_cls.fix_date_format(
                    self.export_methods_cls.infant_crf_data(crf_obj))
                data.update(panel_name=crf_obj.panel.name)
                if data['panel_name'] in karabo_panels:
                    data['protocol_number'] = '108'
                for e_fields in exclude_fields:
                    try:
                        del data[e_fields]
                    except KeyError:
                        pass
                crf_data.append(data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_infant_' + crf_name + '_' + timestamp + '.csv'
            if not os.path.exists(self.infant_export_path):
                os.makedirs(self.infant_export_path)
            final_path = self.infant_export_path + fname
            df_crf = pd.DataFrame(crf_data)
            df_crf.to_csv(final_path, encoding='utf-8', index=False)

    def maternal_requisitions(self):
        # Export Maternal Requisition data
        crf_list = [
            'maternalrequisition',
        ]

        for crf_name in crf_list:
            crf_cls = django_apps.get_model('td_maternal', crf_name)
            objs = crf_cls.objects.all()
            count = 0
            crf_data = []
            for crf_obj in objs:
                data = self.export_methods_cls.fix_date_format(
                    self.export_methods_cls.maternal_crf_data_dict(crf_obj))
                data.update(panel_name=crf_obj.panel.name)
                for e_fields in exclude_fields:
                    try:
                        del data[e_fields]
                    except KeyError:
                        pass
                try:
                    del data['drawn_datetime']
                    del data['received_datetime']
                except KeyError:
                    pass
                crf_data.append(data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_maternal_' + crf_name + '_' + timestamp + '.csv'
            if not os.path.exists(self.maternal_export_path):
                os.makedirs(self.maternal_export_path)
            final_path = self.maternal_export_path + fname
            df_crf = pd.DataFrame(crf_data)
            df_crf.to_csv(final_path, encoding='utf-8', index=False)
