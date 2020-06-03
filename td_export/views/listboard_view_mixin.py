import datetime
import os
import shutil
import threading
import time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from ..export_data_mixin import ExportDataMixin
from ..export_karabo_data import ExportKaraboData
from ..export_methods import ExportMethods
from ..export_model_lists import (
    maternal_crfs_list, maternal_inlines_dict, maternal_many_to_many_crf,
    infant_inlines_dict, infant_crf_list, infant_many_to_many_crf,
    infant_model_list, maternal_model_list, death_report_prn_model_list,
    offstudy_prn_model_list, maternal_many_to_many_non_crf, karabo_infant_crf_list,
    karabo_maternal_model_list)
from ..export_non_crfs import ExportNonCrfData
from ..export_requisitions import ExportRequisitionData
from ..models import ExportFile


class ListBoardViewMixin:

    def export_maternal_data(self, export_path=None):
            """Export all maternal CRF data.
            """

            export_crf_data = ExportDataMixin(export_path=export_path)
            export_crf_data.export_crfs(
                crf_list=maternal_crfs_list,
                crf_data_dict=ExportMethods().maternal_crf_data_dict,
                study='td_maternal')
            export_crf_data.export_inline_crfs(
                inlines_dict=maternal_inlines_dict,
                crf_data_dict=ExportMethods().maternal_crf_data_dict,
                study='td_maternal')
            export_crf_data.generate_m2m_crf(
                m2m_class=maternal_many_to_many_crf,
                crf_data_dict=ExportMethods().maternal_crf_data_dict,
                study='td_maternal')

    def export_infant_data(self, export_path=None):
        """Export infant data.
        """
        export_crf_data = ExportDataMixin(export_path=export_path)
        export_crf_data.export_crfs(
            crf_list=infant_crf_list,
            crf_data_dict=ExportMethods().infant_crf_data,
            study='td_infant')
        export_crf_data.export_inline_crfs(
            inlines_dict=infant_inlines_dict,
            crf_data_dict=ExportMethods().infant_crf_data,
            study='td_infant')
        ExportDataMixin(export_path=export_path).generate_m2m_crf(
            m2m_class=infant_many_to_many_crf,
            crf_data_dict=ExportMethods().infant_crf_data,
            study='td_infant')

    def export_karabo_infant_data(self, export_path=None):
        """Export infant karabo data.
        """
        infant_karabo_crf_data = ExportKaraboData(export_path=export_path)
        infant_karabo_crf_data.infant_karabo_m2m_crf()
        export_crf_data = ExportDataMixin(export_path=export_path)
        export_crf_data.export_crfs(
            crf_list=karabo_infant_crf_list,
            crf_data_dict=ExportMethods().infant_crf_data,
            study='td_infant')

    def export_karabo_non_crf_data(self, export_path=None):
        """Export both infant and maternal non CFR data.
        """
        non_crf_data = ExportNonCrfData(export_path=export_path)
        non_crf_data.maternal_non_crfs(maternal_model_list=karabo_maternal_model_list,
                                       exclude='ineligibility')

    def export_non_crf_data(self, export_path=None):
        """Export both infant and maternal non CFR data.
        """
        non_crf_data = ExportNonCrfData(export_path=export_path)
        non_crf_data.infant_non_crf(infant_model_list=infant_model_list)
        non_crf_data.death_report(death_report_prn_model_list=death_report_prn_model_list)
        non_crf_data.maternal_non_crfs(maternal_model_list=maternal_model_list)
        non_crf_data.maternal_m2m_non_crf(maternal_many_to_many_non_crf=maternal_many_to_many_non_crf)
        non_crf_data.infant_visit()
        non_crf_data.maternal_visit()
        non_crf_data.offstudy(offstudy_prn_model_list=offstudy_prn_model_list)

    def export_requisitions(self, maternal_export_path=None, infant_export_path=None):
        """Export infant and maternal requisitions.
        """
        requisition_data = ExportRequisitionData(
            maternal_export_path=maternal_export_path,
            infant_export_path=infant_export_path)
        requisition_data.infant_requisitions()
        requisition_data.maternal_requisitions()

    def download_karabo_data(self):
        """Export all data.
        """
        export_identifier = self.identifier_cls().identifier

        last_doc = ExportFile.objects.filter(
            study='karabo', download_complete=True).order_by(
                'created').last()

        options = {
            'description': 'Tshilo Dikotla Export',
            'study': 'karabo',
            'export_identifier': export_identifier,
            'download_time': last_doc.download_time
        }
        doc = ExportFile.objects.create(**options)

        try:
            start = time.clock()
            today_date = datetime.datetime.now().strftime('%Y%m%d')

            zipped_file_path = 'documents/' + export_identifier + '_karabo_export_' + today_date + '.zip'
            dir_to_zip = settings.MEDIA_ROOT + '/documents/' + export_identifier + '_karabo_export_' + today_date

            export_path = dir_to_zip + '/infant/'
            self.export_karabo_infant_data(export_path=export_path)

            export_path = dir_to_zip + '/non_crf/'
            self.export_karabo_non_crf_data(export_path=export_path)

            doc.document = zipped_file_path
            doc.save()

            self.zipfile(
                dir_to_zip=dir_to_zip, start=start,
                export_identifier=export_identifier,
                doc=doc, study='karabo')
        except Exception as e:
            try:
                del_doc = ExportFile.objects.get(
                    description='Tshilo Dikotla Export',
                    study='karabo',
                    export_identifier=export_identifier)
            except ExportFile.DoesNotExist:
                pass
            else:
                del_doc.delete()

    def download_all_data(self):
        """Export all data.
        """

        export_identifier = self.identifier_cls().identifier

        last_doc = ExportFile.objects.filter(
            study='tshilo dikotla', download_complete=True).order_by(
                'created').last()

        options = {
            'description': 'Tshilo Dikotla Export',
            'study': 'tshilo dikotla',
            'export_identifier': export_identifier,
            'download_time': last_doc.download_time
        }
        doc = ExportFile.objects.create(**options)

        try:
            start = time.clock()
            today_date = datetime.datetime.now().strftime('%Y%m%d')

            zipped_file_path = 'documents/' + export_identifier + '_td_export_' + today_date + '.zip'
            dir_to_zip = settings.MEDIA_ROOT + '/documents/' + export_identifier + '_td_export_' + today_date

            export_path = dir_to_zip + '/maternal/'
            self.export_maternal_data(export_path=export_path)

            export_path = dir_to_zip + '/infant/'
            self.export_infant_data(export_path=export_path)

            export_path = dir_to_zip + '/non_crf/'
            self.export_non_crf_data(export_path=export_path)

            maternal_export_path = dir_to_zip + '/maternal/'
            infant_export_path = dir_to_zip + '/infant/'

            self.export_requisitions(
                maternal_export_path=maternal_export_path,
                infant_export_path=infant_export_path)

            doc.document = zipped_file_path
            doc.save()

            # Zip the file

            self.zipfile(
                dir_to_zip=dir_to_zip, start=start,
                export_identifier=export_identifier,
                doc=doc, study='tshilo dikotla')
        except Exception as e:
            try:
                del_doc = ExportFile.objects.get(
                    description='Tshilo Dikotla Export',
                    study='tshilo dikotla',
                    export_identifier=export_identifier)
            except ExportFile.DoesNotExist:
                print(e)
            else:
                del_doc.delete()

    def zipfile(
            self, dir_to_zip=None, start=None,
            export_identifier=None, doc=None, study=None):
        """Zip file.
        """
        # Zip the file

        doc.download_complete = True
        doc.save()

        if not os.path.isfile(dir_to_zip):
            shutil.make_archive(dir_to_zip, 'zip', dir_to_zip)
            # Create a document object.

            end = time.clock()
            download_time = end - start
            try:
                doc = ExportFile.objects.get(
                    export_identifier=export_identifier)
            except ExportFile.DoesNotExist:
                raise ValidationError('Export file is missing for id: ',
                                      export_identifier)
            else:
                doc.download_time = download_time
                doc.save()

            # Notify user the download is done
            subject = study + ' ' + export_identifier + ' Export'
            message = (study + ' ' + export_identifier +
                       ' export files have been successfully generated and '
                       'ready for download. This is an automated message.')
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # FROM
                [self.request.user.email],  # TO
                fail_silently=False)
            threading.Thread(target=self.stop_main_thread)

