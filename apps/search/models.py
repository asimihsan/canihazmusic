from django.db import models
from django.utils import timezone

from jsonfield import JSONField
from uuidfield import UUIDField

class Search(models.Model):
    query = models.CharField(max_length=100)
    genre_exact = JSONField()
    artist_exact = JSONField()
    TYPE_CHOICE = (
        ('all', 'All'),
        ('release', 'Release'),
        ('artist', 'Artist'),
        ('label', 'Label'),
    )
    type_lookup = dict(TYPE_CHOICE)
    type = models.CharField(max_length=8, choices=TYPE_CHOICE)

    uuid = UUIDField(auto=True, db_index=True)
    is_finished = models.BooleanField(default=False)
    results_as_json = models.TextField(blank=True)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # --------------------------------------------------------------------
        #   Update the audit timestamp.
        # --------------------------------------------------------------------
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        # --------------------------------------------------------------------

        super(Search, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode("query: '%s'" % self.query)

    @models.permalink
    def get_absolute_url(self):
        return ('apps.search.views.read_search', (), {'uuid': unicode(self.uuid)})

