from django.db import models
import uuid


class Feature(models.Model):
    """
    Model representing a feature request that users can vote on.

    Features are ordered by vote count (descending) and creation date.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the feature",
    )
    title = models.CharField(max_length=200, help_text="Title of the feature request")
    description = models.TextField(
        blank=True, help_text="Optional detailed description of the feature"
    )
    votes = models.IntegerField(
        default=0, help_text="Number of votes this feature has received"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the feature was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the feature was last updated"
    )

    class Meta:
        ordering = ["-votes", "-created_at"]
        verbose_name = "Feature Request"
        verbose_name_plural = "Feature Requests"

    def __str__(self):
        return f"{self.title} ({self.votes} votes)"

    def upvote(self):
        """Increment the vote count by 1."""
        self.votes += 1
        self.save()
