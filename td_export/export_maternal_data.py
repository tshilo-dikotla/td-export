import pandas as pd, datetime, os

from django.apps import apps as django_apps


from .export_methods import ExportMethods
from .export_model_lists import exclude_fields


class ExportMaternalCrfData:
    """Export data.
    """

    def __init__(self, export_path=None):
        self.export_path = export_path or django_apps.get_app_config('td_export').maternal_path
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        self.export_methods_cls = ExportMethods()

    def matermal_crfs(self, maternal_crfs_list=None):
        """Export all crfs.
        """

        for crf_name in maternal_crfs_list:
            crf_cls = django_apps.get_model('td_maternal', crf_name)
            objs = crf_cls.objects.all()
            count = 0
            crf_data = []
            for crf_obj in objs:
                temp_data = self.export_methods_cls.maternal_crf_data_dict(
                    crf_obj=crf_obj)
                data = self.export_methods_cls.fix_date_format(
                    obj_dict=temp_data)
                for e_fields in exclude_fields:
                    try:
                        del data[e_fields]
                    except KeyError:
                        pass
                crf_data.append(data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_maternal_' + crf_name + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf = pd.DataFrame(crf_data)
            df_crf.to_csv(final_path, encoding='utf-8', index=False)

    def export_maternal_inline_crfs(self, maternal_inlines_dict=None):
        """Export Maternal Inline data.
        """

        for crf_name, inline_n_field in maternal_inlines_dict.items():
            inline, filed_n = inline_n_field
            inline_cls = django_apps.get_model('td_maternal', inline)
            inline_objs = inline_cls.objects.all()
            crf_cls = django_apps.get_model('td_maternal', crf_name)
            count = 0
            mergered_data = []
            crf_objs = crf_cls.objects.all()
            for crf_obj in crf_objs:
                inline_objs = inline_cls.objects.filter(**{filed_n: crf_obj.id})
                if inline_objs:
                    for inline_obj in inline_objs:
                        in_data = inline_obj.__dict__
                        del in_data['_state']

                        crfdata = self.export_methods_cls.maternal_crf_data_dict(
                            crf_obj=crf_obj)

                        # Merged inline and CRF data
                        data = self.export_methods_cls.fix_date_format(obj_dict={**crfdata, **in_data})
                        for e_fields in exclude_fields:
                            try:
                                del data[e_fields]
                            except KeyError:
                                pass
                        mergered_data.append(data)
                        count += 1
                else:
                    temp_data = self.export_methods_cls.maternal_crf_data_dict(
                        crf_obj=crf_obj)
                    crfdata = self.export_methods_cls.fix_date_format(obj_dict=temp_data)
                    for e_fields in exclude_fields:
                        try:
                            del crfdata[e_fields]
                        except KeyError:
                            pass
                    mergered_data.append(crfdata)
                    count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_maternal_' + crf_name + '_' + 'merged' '_' + inline + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf_inline = pd.DataFrame(mergered_data)
            df_crf_inline.to_csv(final_path, encoding='utf-8', index=False)

    def maternal_m2m_crf(self, maternal_many_to_many_crf=None):
        """.
        """

        for crf_infor in maternal_many_to_many_crf:
            crf_name, mm_field, _ = crf_infor
            crf_cls = django_apps.get_model('td_maternal', crf_name)
            count = 0
            mergered_data = []
            crf_objs = crf_cls.objects.all()
            for crf_obj in crf_objs:
                mm_objs = getattr(crf_obj, mm_field).all()
                if mm_objs:
                    for mm_obj in mm_objs:
                        mm_data = mm_obj.__dict__

                        crfdata = self.export_methods_cls.maternal_crf_data_dict(crf_obj=crf_obj)

                        # Merged many to many and CRF data
                        data = self.export_methods_cls.fix_date_format({**crfdata, **mm_data})
                        for e_fields in exclude_fields:
                            try:
                                del data[e_fields]
                            except KeyError:
                                pass
                        mergered_data.append(data)
                        count += 1
                else:
                    crfdata = self.export_methods_cls.fix_date_format(
                        self.export_methods_cls.maternal_crf_data_dict(crf_obj=crf_obj))
                    for e_fields in exclude_fields:
                        try:
                            del crfdata[e_fields]
                        except KeyError:
                            pass
                    mergered_data.append(crfdata)
                    count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'td_maternal_' + crf_name + '_' + 'merged' '_' + mm_field + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf_many2many = pd.DataFrame(mergered_data)
            df_crf_many2many.to_csv(final_path, encoding='utf-8', index=False)
