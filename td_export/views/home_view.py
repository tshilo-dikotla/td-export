from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin


class HomeView(EdcBaseViewMixin, TemplateView):

    template_name = 'td_export/home.html'
