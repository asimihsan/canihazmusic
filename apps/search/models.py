from django.db import models
from django.utils import timezone

from uuidfield import UUIDField

class Search(models.Model):
    uuid = UUIDField(auto=True, db_index=True)
    query = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)
    results_as_json = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # --------------------------------------------------------------------
        #   Update the audit timestamp.
        # --------------------------------------------------------------------
        if not self.id:
            self.created = timezone.now()
        # --------------------------------------------------------------------

        super(Search, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode("query: '%s'" % self.query)

    @models.permalink
    def get_absolute_url(self):
        return ('apps.search.views.read_search', (), {'uuid': unicode(self.uuid)})

