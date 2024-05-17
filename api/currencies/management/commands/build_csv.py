from django.core.management.base import BaseCommand
from currencies.models import HistoryCurrencies
import typing
import csv
from api import settings
from django.utils import timezone


class Command(BaseCommand):
    help = "Export current exchange rates to csv file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the CSV file",
            nargs="?",
            default=settings.DEFAULT_CSV_PATH,
        )

    def handle(self, *args: typing.Tuple, **options: typing.Dict):
        file_path = options["file_path"]

        current_time = timezone.now()
        queryset = HistoryCurrencies.objects.filter(
            date__lt=current_time, actualy_end__gt=current_time
        )
        if queryset:
            raw_data = queryset.values()
            fields = tuple(raw_data[0].keys())

            with open(file_path, "w", encoding="utf-8") as file:
                csvwriter = csv.DictWriter(file, fieldnames=fields)
                csvwriter.writeheader()
                csvwriter.writerows(raw_data)
                self.stdout.write(
                    self.style.SUCCESS(f"Successed export to csv to {file_path}")
                )

        else:
            self.stdout.write(self.style.INFO("Current currencies not found"))
