

from django.views import generic
from django.forms import ModelForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from preview.models import Email


class PreviewForm(ModelForm):
	""" Use for creating/editing email previews."""
	class Meta:
		model = Email
		fields = ['sender', 'subject', 'body', 'date']


class IndexView(generic.ListView):
	# model = Email  ## don't need this with the get_queryset method
	template_name = 'preview/index.html'
	context_object_name = 'email_list'

	def get_queryset(self):
		# filter this later...
		return Email.objects.all()


class DetailView(generic.DetailView):

	model = Email
	template_name = 'preview/detail.html'
	context_object_name = 'preview_object'


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