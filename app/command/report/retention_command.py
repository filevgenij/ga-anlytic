from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvWriter


class RetentionCommand(BaseCommand):
    """
    Calculate retentions for 2017

    report:retention
        {--path=: Path to result csv file. }
        {--only-paid-search=False : Calculate only for paid users}
    """
    def handle(self):

        retention = self.get_container()['retention']
        only_paid_search = (self.option('only-paid-search') == 'True')

        report_data = retention.get_report(only_paid_search)

        for i, _ in enumerate(report_data):
            if i == 0:
                report_data[i].insert(0, 'Registrations')
            else:
                report_data[i].insert(0, 'Unique logins in a month {}'.format(i))

        header = [
            '', 'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'September', 'October',
            'November', 'December'
        ]
        report_data.insert(0, header)

        CsvWriter.write_data(self.option('path'), report_data, '|')
