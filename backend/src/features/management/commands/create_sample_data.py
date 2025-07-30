from django.core.management.base import BaseCommand
from features.models import Feature


class Command(BaseCommand):
    help = "Create sample feature data for testing"

    def handle(self, *args, **options):
        # Create sample features
        sample_features = [
            {
                "title": "Dark Mode Support",
                "description": "Add dark mode theme option for better user experience during night time usage.",
                "votes": 15,
            },
            {
                "title": "Mobile App",
                "description": "Develop native mobile applications for iOS and Android platforms.",
                "votes": 23,
            },
            {
                "title": "Real-time Notifications",
                "description": "Push notifications for new features and voting updates.",
                "votes": 8,
            },
            {
                "title": "Advanced Search",
                "description": "Enhanced search functionality with filters and sorting options.",
                "votes": 12,
            },
            {
                "title": "User Profiles",
                "description": "Allow users to create profiles and track their feature requests.",
                "votes": 6,
            },
        ]

        created_count = 0
        for feature_data in sample_features:
            feature, created = Feature.objects.get_or_create(
                title=feature_data["title"],
                defaults={
                    "description": feature_data["description"],
                    "votes": feature_data["votes"],
                },
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created feature: {feature.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} sample features")
        )
