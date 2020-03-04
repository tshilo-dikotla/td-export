import pandas as pd, datetime, os

from django.apps import apps as django_apps


from .export_methods import ExportMethods
from .export_model_lists import exclude_fields


class ExportKaraboData:
    """Export data.
    """
    
    def __init__(self, export_path=None):
        self.export_path = export_path or django_apps.get_app_config('td_export').maternal_path
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        self.export_methods_cls = ExportMethods()
    
    
    def infant_karabo_m2m_crf(self):
        # Export Infant Many-to-Many data
        karabo_crfs_dict = {
            'karabotuberculosishistory': [
                'coughing_rel',
                'fever_rel',
                'weight_loss_rel',
                'night_sweats_rel',
                'diagnosis_rel', ]
            }
        for crf_name, field_model in karabo_crfs_dict.items():
            crf_cls = django_apps.get_model('td_infant', crf_name)
            count = 0
            mergered_data = []
            crf_objs = crf_cls.objects.all()
            for crf_obj in crf_objs:
                crfdata = self.export_methods_cls.infant_crf_data(crf_obj)
                for mm_field_name in field_model:

                    mm_objs = getattr(crf_obj, mm_field_name).all()
                    mm_data = ''
                    if mm_objs:
                        count = 0
                        for mm_obj in mm_objs:
                            mm_data += mm_obj.short_name
                            count += 1
                            if count < mm_objs.count():
                                mm_data += '~'
                        data = self.export_methods_cls.fix_date_format({**crfdata})
                        data[mm_field_name] = mm_data
                        mergered_data.append(data)
                        count += 1
                    else:
                        data = self.export_methods_cls.fix_date_format({**crfdata})
                        data[mm_field_name] = None
                        for e_fields in exclude_fields:
                            try:
                                del data[e_fields]
                            except KeyError:
                                pass
                        mergered_data.append(data)
                        count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_maternal_' + crf_name + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf_inline = pd.DataFrame(mergered_data)
            df_crf_inline.to_csv(final_path, encoding='utf-8', index=False)