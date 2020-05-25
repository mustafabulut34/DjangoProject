from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.http import HttpResponseRedirect
from .models import Comment, CommentForm


def index(request):
    return render(request, 'index.html', {})


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = get_user(request)
            data = Comment()
            data.user_id = current_user.id
            data.room_id = id
            data.rate = form.cleaned_data['rate']
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Thank you!")
            return HttpResponseRedirect(url)
    messages.warning(request, "Failed!")
    return HttpResponseRedirect(url)
