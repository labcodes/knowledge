from django.views.generic import View
from django.shortcuts import redirect


# class IndexView(ListView):
#     model = Link
#     context_object_name = 'links'
#     paginate_by = settings.LINKS_PER_PAGE
#     template_name = 'links/index.html'

class IndexView(View):

    def get(self, request):
        return redirect('/links')
