import json
import unicodedata
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.apps import apps

class Command(BaseCommand):
    help = 'Dump data with UTF-8 encoding, filtering problematic characters.'

    def handle(self, *args, **kwargs):
        all_data = []
        for model in apps.get_models():
            queryset = model.objects.all()
            if queryset.exists():
                # Serialize model data to JSON
                serialized_data = json.loads(serialize("json", queryset))
                # Clean problematic characters
                for obj in serialized_data:
                    for field, value in obj['fields'].items():
                        if isinstance(value, str):
                            # Remove problematic characters
                            obj['fields'][field] = ''.join(
                                ch for ch in value if unicodedata.category(ch)[0] != 'C'
                            )
                all_data.extend(serialized_data)

        # Write data to JSON file
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Data exported successfully to data.json'))
