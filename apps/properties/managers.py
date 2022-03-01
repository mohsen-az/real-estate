from django.db.models import Manager


class PropertyPublishedManager(Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(published_status=True)
