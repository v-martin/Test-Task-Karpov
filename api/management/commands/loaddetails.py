import csv
from datetime import datetime

from django.core.management import BaseCommand
from loguru import logger

from api.models import Sale, Detail


class Command(BaseCommand):

    def handle(self, *args, **options):
        counter = 0
        with open('df_sales_detail.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                counter += 1
                detail, is_created = Detail.objects.get_or_create(
                    sale_id_id=int(row[1]),
                    good=row[2],
                    price=int(row[3]),
                    date=datetime.strptime(row[4], '%Y-%m-%d %H%M%S'),
                    user_id=row[5]
                )
                if is_created:
                    logger.debug(f'Detail of order {detail.sale_id} created!')
                else:
                    logger.debug(f'Detail of order {detail.sale_id} already exists!')
                if counter > 1000:
                    return
