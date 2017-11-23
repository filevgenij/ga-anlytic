from app.utils.base_command import BaseCommand
from app.utils.hepler.date import DateHelper


class LoadSceneCommand(BaseCommand):
    """
    Load scenes from GA

    ga:load:scene
        {--from= : Date from in format YYYY-MM-DD}
        {--to= : Date to in format YYYY-MM-DD}
        {--step=1: Step for date range}
    """
    def handle(self):
        collector = self.get_container()['collector']

        dates_ranges = DateHelper.split_period([self.option('from'),
                                                self.option('to')],
                                               int(self.option('step')))
        self.line("Split to {} ranges".format(len(dates_ranges)))

        for dates_range in dates_ranges:
            self.line("Collect {} - {}...\n".format(dates_range[0], dates_range[1]))
            collector.collect_scene(dates_range, self.progress_bar())
            self.line("\n")

        self.line('Done!')
