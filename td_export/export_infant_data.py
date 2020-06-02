import datetime
import os

from django.apps import apps as django_apps

import pandas as pd

from .export_methods import ExportMethods
from .export_model_lists import exclude_fields, exclude_m2m_fields


class ExportInfantCrfData:
    """Export data.
    """

    def __init__(self, export_path=None):
        self.export_path = export_path or django_apps.get_app_config('td_export').infant_path
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        self.export_methods_cls = ExportMethods()

    def export_infant_crfs(self, infant_crf_list=None):
        """Export infant crf data.
        """

        for crf_name in infant_crf_list:
            crf_cls = django_apps.get_model('td_infant', crf_name)
            objs = crf_cls.objects.all()
            count = 0
            crf_data = []
            for crf_obj in objs:
                data = self.export_methods_cls.fix_date_format(
                    self.export_methods_cls.infant_crf_data(crf_obj))
                for e_fields in exclude_fields:
                    try:
                        del data[e_fields]
                    except KeyError:
                        pass
                crf_data.append(data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_infant_' + crf_name + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf = pd.DataFrame(crf_data)
            df_crf.to_csv(final_path, encoding='utf-8', index=False)

    def export_infant_inline(self, infant_inlines_dict=None):
        """Export inline data.
        """

        for crf_name, inline_n_field in infant_inlines_dict.items():
            inline, filed_n = inline_n_field
            for inl in inline:
                inline_cls = django_apps.get_model('td_infant', inl)
                inline_objs = inline_cls.objects.all()
                crf_cls = django_apps.get_model('td_infant', crf_name)
                count = 0
                mergered_data = []
                crf_objs = crf_cls.objects.all()
                for crf_obj in crf_objs:
                    inline_objs = inline_cls.objects.filter(**{filed_n: crf_obj.id})
                    if inline_objs:
                        for inline_obj in inline_objs:
                            in_data = inline_obj.__dict__
                            del in_data['_state']

                            crfdata = self.export_methods_cls.infant_crf_data(crf_obj)

                            # Merged inline and CRF data
                            data = self.export_methods_cls.fix_date_format({**crfdata, **in_data})
                            for e_fields in exclude_fields:
                                try:
                                    del data[e_fields]
                                except KeyError:
                                    pass
                            mergered_data.append(data)
                            count += 1
                    else:
                        crfdata = self.export_methods_cls.fix_date_format(
                            self.export_methods_cls.infant_crf_data(crf_obj))
                        for e_fields in exclude_fields:
                            try:
                                del crfdata[e_fields]
                            except KeyError:
                                pass
                        mergered_data.append(crfdata)
                        count += 1
                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                fname = 'td_infant_' + crf_name + '_' + 'merged' '_' + inl + '_' + timestamp + '.csv'
                final_path = self.export_path + fname
                df_crf_inline = pd.DataFrame(mergered_data)
                df_crf_inline.to_csv(final_path, encoding='utf-8', index=False)

    def infant_m2m_crf(self, infant_many_to_many_crf=None):
        # Export Infant Many-to-Many data

        for crf_infor in infant_many_to_many_crf:
            crf_name, mm_field, _ = crf_infor
            crf_cls = django_apps.get_model('td_infant', crf_name)
            count = 0
            mergered_data = []
            crf_objs = crf_cls.objects.all()
            for crf_obj in crf_objs:

                crfdata = self.export_methods_cls.infant_crf_data(crf_obj)
                data = self.export_methods_cls.fix_date_format({**crfdata})

                exclude_m2m_fields.append('study_status')
                for e_fields in exclude_m2m_fields:
                    try:
                        del data[e_fields]
                    except KeyError:
                        pass
                data[mm_field] = None
                mm_field_data = ''

                mm_objs = getattr(crf_obj, mm_field).all()
                if mm_objs:
                    for mm_obj in mm_objs:

                        mm_field_data += mm_obj.short_name
                        count += 1
                        if count < mm_objs.count():
                            mm_field_data += ','
                        data[mm_field] = mm_field_data
                mergered_data.append(data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_infant_' + crf_name + '_' + 'merged' '_' + mm_field + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf_inline = pd.DataFrame(mergered_data)
            df_crf_inline.to_csv(final_path, encoding='utf-8', index=False)
