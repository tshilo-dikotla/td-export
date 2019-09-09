import datetime, os, re, time, threading, shutil
from django.conf import settings
from django.contrib import messages

from edc_base.view_mixins import EdcBaseViewMixin

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ..model_wrappers import ExportFileModelWrapper
from ..export_maternal_data import ExportMaternalCrfData
from ..export_infant_data import ExportInfantCrfData
from ..export_non_crfs import ExportNonCrfData
from ..export_requisitions import ExportRequisitionData
from ..export_model_lists import (
    maternal_crfs_list, maternal_inlines_dict, infant_crf_list,
    infant_inlines_dict, infant_many_to_many_crf, infant_model_list,
    maternal_model_list, maternal_many_to_many_crf, death_report_prn_model_list,
    offstudy_prn_model_list)
from ..models import ExportFile
from ..identifiers import ExportIdentifier


class ListBoardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin, ListboardView):

    listboard_template = 'export_listboard_template'
    listboard_url = 'export_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'td_export.exportfile'
    model_wrapper_cls = ExportFileModelWrapper
    identifier_cls = ExportIdentifier
    navbar_name = 'td_export'
    navbar_selected_item = 'export_data'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'export_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def export_maternal_data(self, export_path=None):
        """Export all maternal CRF data.
        """
        crf_data = ExportMaternalCrfData(export_path=export_path)
        crf_data.matermal_crfs(maternal_crfs_list=maternal_crfs_list)
        crf_data.export_maternal_inline_crfs(maternal_inlines_dict=maternal_inlines_dict)

    def export_infant_data(self, export_path=None):
        """Export infant data.
        """
        infant_crf_data = ExportInfantCrfData(export_path=export_path)
        infant_crf_data.export_infant_crfs(infant_crf_list=infant_crf_list)
        infant_crf_data.export_infant_inline(infant_inlines_dict=infant_inlines_dict)
        infant_crf_data.infant_m2m_crf(infant_many_to_many_crf=infant_many_to_many_crf)

    def export_non_crf_data(self, export_path=None):
        """Export both infant and maternal non CFR data.
        """
        non_crf_data = ExportNonCrfData(export_path=export_path)
        non_crf_data.infant_non_crf(infant_model_list=infant_model_list)
        non_crf_data.death_report(death_report_prn_model_list=death_report_prn_model_list)
        non_crf_data.maternal_non_crfs(maternal_model_list=maternal_model_list)
        non_crf_data.maternal_m2m_non_crf(maternal_many_to_many_crf=maternal_many_to_many_crf)
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

    def stop_main_thread(self):
        """Stop export file generation thread.
        """
        time.sleep(20)
        threads = threading.enumerate()
        threads = [t for t in threads if t.is_alive()]
        for thread in threads:
            if thread.name == 'td_export':
                thread._stop()

    def download_all_data(self):
        """Export all data.
        """
        today_date = datetime.datetime.now().strftime('%Y%m%d')
        export_identifier = self.identifier_cls().identifier
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
        
        # Zip the file
        
        if not os.path.isfile(dir_to_zip):
            shutil.make_archive(dir_to_zip,'zip',dir_to_zip)
            # Create a document object.
            options = {
                'description':'Tshilo Dikotla' + ' Export',
                'export_identifier': export_identifier
                }
            doc = ExportFile.objects.create(**options)
            doc.document = zipped_file_path
            doc.save()

            # Notify user the download is done
            self.request.user.email_user(
                'td export', 'Tshilo Dikotla export files have been successfully generated and ready for download.')
            threading.Thread(target=self.stop_main_thread)
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        download = self.request.GET.get('download')
        active_download = False
        if download == '1':
            threads = threading.enumerate()
            threads = [t for t in threads if t.is_alive()]
            if threads:
                for thread in threads:
                    if thread.is_alive() and thread.name == 'td_export':
                        active_download = True
                        messages.add_message(
                            self.request, messages.INFO,
                                ('Download that was initiated is still running please wait until an export is fully prepared.'))
            if not active_download:
                download_thread = threading.Thread(name='td_export', target=self.download_all_data)
                download_thread.start()
                 
                messages.add_message(
                        self.request, messages.INFO,
                        ('Download initiated, you will receive an email once the download is completed.'))
        context.update(
            export_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('export_identifier'):
            options.update(
                {'export_identifier': kwargs.get('export_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
