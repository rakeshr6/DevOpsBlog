import django_filters

from tempcheck.models import Post

class PostFilter(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        for key in self.get_filters():
            self.form.fields[key].widget.attrs['class'] = 'form-control'
            self.form.fields['title__icontains'].label = "Search"

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }

