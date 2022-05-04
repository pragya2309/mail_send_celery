from django.shortcuts import render
from .task import send_mail_fun
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.views.generic import ListView
from django.template.context_processors import csrf
from django.conf.urls import url
from .form import GenerateRandomUserForm,UserRegistrationForm
from .task import create_random_user_accounts


def send_mail_to_all(request):
    send_mail_fun.delay()
    return HttpResponse("sent")
    

class GenerateRandomUserView(FormView):
    template_name = 'generate_random_user.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')
    
class UsersListView(ListView):
    template_name = 'user_list.html'
    model = User



def register(request, register_form=UserRegistrationForm):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(email=request.POST.get('email'), password=request.POST.get('password1'))

            if user:
                messages.success(request, "You have successfully registered")
                return redirect(reverse('profile'))

            else:
                messages.error(request, "unable to log you in at this time!")

    else:
        form = register_form()

    args = {'form':form}
    args.update(csrf(request))

    return render(request, 'register.html', args)


def url_shortner(request):
    if request.method == 'POST':
        form = Url(request.POST)
        if form.is_valid():
            slug = ''.join(random.choice(string.ascii_letters)
                           for x in range(10))
            url = form.cleaned_data["url"]
            new_url = UrlData(url=url, slug=slug)
            new_url.save()
            request.user.urlshort.add(new_url)
            return redirect('/')
    else:
        form = Url()
    data = UrlData.objects.all()
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'index.html', context)


def urlRedirect(request, slugs):
    data = UrlData.objects.get(slug=slugs)
    return redirect(data.url)