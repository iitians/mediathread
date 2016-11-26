from django.db import models
from django.contrib.auth.models import User
from courseaffils.models import Course
from mediathread.djangosherd.models import SherdNote


class SequenceAsset(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    # The course foreign key refers to which course the SequenceAsset
    # belongs to as a general Mediathread asset independent of the
    # assignment (project) structure. SequenceAssets that are created
    # as responses to a Sequence assignment are already associated
    # with a course via the Project, through the
    # ProjectSequenceAssignment model, so this field is superfluous
    # for those SequenceAssets.
    course = models.ForeignKey(Course)
    spine = models.ForeignKey(SherdNote, blank=True, null=True)

    def update_track_elements(self, media_elements, text_elements):
        """Updates the SequenceAsset's track elements.

        Takes media_elements and text_elements as JSON-style objects and
        creates Django objects.
        """
        SequenceMediaElement.objects.filter(sequence_asset=self).delete()
        a = []
        for track_data in media_elements:
            a.append(SequenceMediaElement(sequence_asset=self, **track_data))
        SequenceMediaElement.objects.bulk_create(a)

        SequenceTextElement.objects.filter(sequence_asset=self).delete()
        a = []
        for track_data in text_elements:
            a.append(SequenceTextElement(sequence_asset=self, **track_data))
        SequenceTextElement.objects.bulk_create(a)


class SequenceMediaElement(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    sequence_asset = models.ForeignKey(
        SequenceAsset,
        related_name='media_elements',
        on_delete=models.CASCADE)
    start_time = models.DecimalField(
        max_digits=12, decimal_places=5)
    end_time = models.DecimalField(
        max_digits=12, decimal_places=5)
    media = models.ForeignKey(SherdNote)


class SequenceTextElement(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    sequence_asset = models.ForeignKey(
        SequenceAsset,
        related_name='text_elements',
        on_delete=models.CASCADE)
    start_time = models.DecimalField(
        max_digits=12, decimal_places=5)
    end_time = models.DecimalField(
        max_digits=12, decimal_places=5)
    text = models.TextField()
