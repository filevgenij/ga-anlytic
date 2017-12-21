from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvWriter


class PaymentPageCommand(BaseCommand):
    """
    Calculate payment page statistic for 2017 year

    report:payment_page
        {--path= : Path to result csv file. It should be absolute path}
    """
    def handle(self):
        payment_page = self.get_container()['payment_page']

        result = payment_page.get_report()

        CsvWriter.write_data(self.option('path'), result, '|')
