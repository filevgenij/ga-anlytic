from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvWriter


class RegistrationWayCommand(BaseCommand):
    """
    Calculate registration way statistic

    report:registration_way
        {--path= : Path to result csv file. }
        {--period=* : Report period. For example "--period 2017-01-01 --period 2017-02-01"}
        {--group-by= : Group result by month, week}
    """
    def handle(self):

        registration_way = self.get_container()['registration_way']

        group_by = self.option('group-by')
        period = self.option('period')
        if group_by == 'month':
            report_data = registration_way.get_report_by_month(period)
            first_column_name = 'Month'
        elif group_by == 'week':
            report_data = registration_way.get_report_by_week(period)
            first_column_name = 'Week'
        else:
            self.line('Choose one of available options for period param - month or week')
            return 0

        header = [
            first_column_name, 'Total Reg', 'From Fb', 'From G+', 'From Li',
            'From email', 'Confirm'
        ]
        report_data.insert(0, header)

        CsvWriter.write_data(self.option('path'), report_data, '|')
