from django.db import models


class JobField(models.Model):

    name = models.CharField(max_length=100)


class JobFieldCluster(models.Model):

    sco_id = models.BigIntegerField()
    job_field = models.ForeignKey(JobField, on_delete=models.CASCADE, related_name='clusters')
