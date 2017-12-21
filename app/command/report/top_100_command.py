from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvWriter


class Top100Command(BaseCommand):
    """
    Calculate top 100 user statistic

    report:top_100
        {--path=: Path to result csv file. }
        {--period=* : Report period. For example "--period 2017-01-01 --period 2017-02-01"}
        {--lang-filter=: Filter by language. For example "en"}
        {--only-paid-search=False: Calculate only for paid users}
    """
    def handle(self):

        top100 = self.get_container()['top100']

        period = self.option('period')
        lang = self.option('lang-filter')
        only_paid_search = (self.option('only-paid-search') == 'True')
        report_data = top100.get_report(period, lang, only_paid_search)

        header = [
            'User ID', 'Email', 'Full Name', 'Country', 'Industry', 'Website',
            'Social network', 'Reg date', 'Payment date', 'Total scenes', 'Total bands',
            'Total download', 'Days Member', 'Unique days with logins',
            'Unique days with login in period', 'Language'
        ]
        report_data.insert(0, header)

        CsvWriter.write_data(self.option('path'), report_data, '|')

