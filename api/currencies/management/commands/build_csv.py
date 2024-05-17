"""
Module providing a Django management command
to export current exchange rates to a CSV file.
This module defines a Django management command,
`export_exchange_rates`, which exports
the current exchange rates stored in the database
to a CSV file specified by the user.
"""

from django.core.management.base import BaseCommand
from currencies.models import HistoryCurrencies
import typing
import csv
from api import settings
from django.utils import timezone
import argparse


class Command(BaseCommand):
    help = "Export current exchange rates to csv file"

    def add_arguments(self, parser: argparse.ArgumentParser):
        """
        Add command-line arguments for the management command.

        Args:
            parser (ArgumentParser): The parser object for parsing
            command-line arguments.

        """
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the CSV file",
            nargs="?",
            default=settings.DEFAULT_CSV_PATH,
        )

    def handle(self, *args: typing.Tuple, **options: typing.Dict):
        """
        Handle the execution of the management command.

        Args:
            args: Positional arguments.
            options: Keyword arguments.

        """
        file_path = options["file_path"]

        current_time = timezone.now()
        queryset = HistoryCurrencies.objects.filter(
            date__lt=current_time, actualy_end__gt=current_time
        )
        if queryset:
            raw_data = queryset.values()
            fields = tuple(raw_data[0].keys())

            with open(file_path, "w", encoding="utf-8") as file:  # type: ignore
                csvwriter = csv.DictWriter(file, fieldnames=fields)
                csvwriter.writeheader()
                csvwriter.writerows(raw_data)
                self.stdout.write(
                    self.style.SUCCESS(f"Successed export to csv to {file_path}")
                )

        else:
            self.stdout.write(self.style.INFO("Current currencies not found"))
