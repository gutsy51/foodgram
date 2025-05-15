import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        file_name = options['json_file']
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'data', file_name)
            with open(json_file_path, encoding='utf-8') as file:
                ingredients = Ingredient.objects.bulk_create(
                    [Ingredient(**item) for item in json.load(file)],
                    ignore_conflicts=True
                )
            self.stdout.write(
                self.style.SUCCESS(f'Добавлено {len(ingredients)} ингредиентов')
            )

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Ошибка загрузки {file_name}: {e}')
            )