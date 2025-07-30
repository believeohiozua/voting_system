from django.core.management.base import BaseCommand
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.generators import SchemaGenerator


class Command(BaseCommand):
    help = "Test OpenAPI schema generation"

    def handle(self, *args, **options):
        try:
            generator = SchemaGenerator()
            schema = generator.get_schema(request=None, public=True)
            self.stdout.write(self.style.SUCCESS("✅ Schema generation successful!"))
            self.stdout.write(f'Schema has {len(schema.get("paths", {}))} paths')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Schema generation failed: {str(e)}")
            )
            import traceback

            traceback.print_exc()
