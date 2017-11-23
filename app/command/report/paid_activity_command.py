from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvWriter


class PaidActivityCommand(BaseCommand):
    """
    Calculate paid Activity statistic

    report:paid_activity
        {--path= : Path to result csv file. It should be absolute path}
    """
    def handle(self):
        paid_activity = self.get_container()['paid_activity']

        result = paid_activity.get_report()

        CsvWriter.write_data(self.option('path'), result, '|')
