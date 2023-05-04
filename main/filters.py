from django.contrib.auth.models import User
import django_filters
from .models import Manga

class MangaFilter(django_filters.FilterSet):
    year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    class Meta:
        model = Manga
        fields = ["title", "type", "description", "publication_date", "author", "created", "status", "age_restriction", ]
