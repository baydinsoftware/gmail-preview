

from django.views import generic
from django.forms import ModelForm, Textarea
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from preview.models import Preview, Comment


# for login_required decorator
login_url = '/preview/login'

class PreviewForm(ModelForm):
    """ Use for creating/editing email previews."""
    class Meta:
        model = Preview
        fields = ['sender', 'subject', 'body', 'date']

class CommentForm(ModelForm):
    """ For adding comments to a Preview."""
    
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea,
        }


class IndexView(generic.ListView):
    """ Main view for existing previews."""
    # model = Email  ## don't need this with the get_queryset method
    template_name = 'preview/index.html'
    context_object_name = 'email_list'

    def get_queryset(self):
        return Preview.objects.all().order_by('-date')


@login_required(login_url=login_url)
def detail(request, pk):
    """ View of a Preview and associated comments. Accepts new comments."""

    preview = get_object_or_404(Preview, pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # don't commit until we've set up the non-user input fields
            new_comment = comment_form.save(commit=False)
            new_comment.date = timezone.now()
            new_comment.preview = preview
            new_comment.commentor = request.user
            # add user information too? ... depends on auth system?
            new_comment.save()
            
            return HttpResponseRedirect(reverse('preview:detail', 
                                                kwargs={'pk': pk}))
    else:
        comment_form = CommentForm()

    comments = Comment.objects.filter(preview=preview)
    context = {
        'preview_object': preview,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'preview/detail.html', context)


@login_required(login_url=login_url)
def new(request):
    """ Form fields for creating/editing a Preview db entry. """
    
    if request.method == 'POST':
        # fill
        form = PreviewForm(request.POST)
        if form.is_valid():
            new_preview = form.save(commit=False)
            new_preview.creator = request.user
            new_preview.save()
            # --> created preview
            return HttpResponseRedirect(reverse('preview:detail', 
                kwargs={'pk': new_preview.id}))
    else:
        # empty form
        form = PreviewForm()

    return render(request, 'preview/new.html', {'form': form})


def register(request):
    """ Form for registering a new User."""

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            # login the user
            user = authenticate(username=request.POST['username'], 
                                password=request.POST['password1'])
            if user is not None:
                login(request, user)
            # else error - but that should never happen
            return HttpResponseRedirect(reverse('preview:index')) # change this to use 'next' field

    else:
        user_form = UserCreationForm()

    return render(request, 'preview/register.html', {'form': user_form})
