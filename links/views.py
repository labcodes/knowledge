from django.urls import reverse_lazy
from django.views.generic.list import ListView

from django.views.generic import CreateView, View

from django.conf import settings

from .models import Link
from .forms import LinkForm


class ListLinksView(ListView):
    model = Link
    context_object_name = 'links'
    paginate_by = settings.LINKS_PER_PAGE
    template_name = 'links/index.html'


class CreateLinkView(CreateView):
    template_name = 'links/create-link-form.html'
    success_url = reverse_lazy('links:list-links')
    form_class = LinkForm


class LoginView(View):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)

            if user is not None:
                login(request, user)

                return redirect(reverse_lazy('links:list-links'))
            else:
                return render(request, 'links/index.html', {'login_error': 'Wrong email or password'})

        except User.DoesNotExist:
            return render(request, 'links/index.html', {'login_error': 'Wrong email or password'})
