from django.db import models
from django.contrib.auth.models import User
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
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_features",
        help_text="User who created this feature request",
    )
    voters = models.ManyToManyField(
        User,
        through="Vote",
        related_name="voted_features",
        help_text="Users who have voted for this feature",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the feature was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the feature was last updated"
    )

    class Meta:
        ordering = ["-vote_count", "-created_at"]
        verbose_name = "Feature Request"
        verbose_name_plural = "Feature Requests"

    def __str__(self):
        return f"{self.title} ({self.vote_count} votes)"

    @property
    def vote_count(self):
        """Get the current vote count."""
        return self.votes.count()

    def upvote(self, user):
        """Add a vote from a user if they haven't voted already."""
        vote, created = Vote.objects.get_or_create(feature=self, user=user)
        return created  # Returns True if vote was created, False if already existed

    def remove_vote(self, user):
        """Remove a user's vote."""
        return Vote.objects.filter(feature=self, user=user).delete()[0] > 0

    def has_user_voted(self, user):
        """Check if a user has voted for this feature."""
        if user.is_anonymous:
            return False
        return self.votes.filter(user=user).exists()


class Vote(models.Model):
    """
    Model representing a vote on a feature by a user.
    """

    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["feature", "user"]  # One vote per user per feature
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return f"{self.user.username} voted for {self.feature.title}"
