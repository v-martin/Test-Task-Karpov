import csv
from datetime import datetime

from django.core.management import BaseCommand
from loguru import logger

from api.models import Sale


class Command(BaseCommand):

    def handle(self, *args, **options):
        counter = 0
        with open('df_sales.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                counter += 1
                sale, is_created = Sale.objects.get_or_create(
                    sale_id=int(row[1]),
                    date=datetime.strptime(row[2], '%d-%m-%y %H:%M'),
                    count_pizza=int(row[3]),
                    count_drink=int(row[4]),
                    price=int(row[5]),
                    user_id=row[6]
                )
                if is_created :
                    logger.debug(f'Sale {sale.sale_id} created!')
                else:
                    logger.debug(f'Sale {sale.sale_id} already exists!')
                if counter > 1000:
                    return


