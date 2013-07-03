

from django.views import generic
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from preview.models import Preview, Comment


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



class IndexView(generic.ListView):
    """ Main view for existing previews."""
    # model = Email  ## don't need this with the get_queryset method
    template_name = 'preview/index.html'
    context_object_name = 'email_list'

    def get_queryset(self):
        # filter this later...
        return Preview.objects.all()

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
        'comment_form': comment_form
    }
    return render(request, 'preview/detail.html', context)

def new(request):
    """ Form fields for creating/editing a Preview db entry

    Todo: implement active jQuery update of gmail repr.
    """

    if request.method == 'POST':
        # fill
        form = PreviewForm(request.POST)
        if form.is_valid():
            new_preview = form.save()
            # --> created preview
            return HttpResponseRedirect(reverse('preview:detail', 
                kwargs={'pk': new_preview.id}))
    else:
        # empty form
        form = PreviewForm()

    return render(request, 'preview/new.html', {'form': form})
