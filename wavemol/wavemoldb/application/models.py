from django.db import models

STATUS_CHOICES = (
    ('QUEUED', 'QUEUED'),
    ('RUNNING', 'RUNNING'),
    ('FAILED', 'FAILED'),
    ('SUCCESS', 'SUCCESS'),
)

class QueuedTask(models.Model):
    type = models.CharField(max_length=1024)
    parameters = models.CharField(max_length=1024)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    def __unicode__(self):
        return str(self.id)+" "+self.status+" : "+self.type+" "+self.parameters


