from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvWriter


class SceneCommand(BaseCommand):
    """
    Calculate scene report 2017

    report:scene
        {--path=: Path to result csv file. }
        {--only-paid-search=False : Calculate only for paid users}
    """
    def handle(self):

        scenes_report = self.get_container()['scenes_report']
        only_paid_search = (self.option('only-paid-search') == 'True')

        scene_metrics = (
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            (1, 10), (11, 50), (51, 100),
            (101, 150), (151, 200), (201, 300),
            (301, 500), (501, 1000), (1001, 10000000)
        )
        report_data = scenes_report.get_report(scene_metrics, only_paid_search)

        header = [
            'Uniques scenes viewed by users who logged in to the system at least once a month',
            'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
        ]
        report_data.insert(0, header)

        CsvWriter.write_data(self.option('path'), report_data, '|')
