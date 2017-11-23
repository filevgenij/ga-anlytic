from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvWriter


class UserInfoSelectBySceneCommand(BaseCommand):
    """
    Calculate top 100 user statistic

    report:user_info_selected_by_scene
        {--path= : Path to result csv file. }
        {--scene-count=: Amount of scene in period}
        {--period=* : Report period. For example "--period 2017-01-01 --period 2017-02-01"}
    """

    def handle(self):

        period = self.option('period')
        user_finder = self.get_container()['user_finder']
        user_ids = user_finder.find_user_ids(int(self.option('scene-count')), period)
        user_info = self.get_container()['user_info']
        report_data = user_info.get_report(user_ids, period)

        header = [
            'User ID', 'Email', 'Full Name', 'Country', 'Industry', 'Website',
            'Social network', 'Reg date', 'Payment date', 'Days Member', 'Unique days with logins',
            'Unique days with login in period'
        ]
        report_data.insert(0, header)

        CsvWriter.write_data(self.option('path'), report_data, '|')
