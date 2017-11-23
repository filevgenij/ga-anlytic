from app.utils.base_command import BaseCommand
from app.utils.hepler.date import DateHelper


class LoadReferrerCommand(BaseCommand):
    """
    Load referrer from GA

    ga:load:referrer
        {--from= : Date from in format YYYY-MM-DD}
        {--to= : Date to in format YYYY-MM-DD}
        {--step=2: Step for date range}
    """
    def handle(self):
        user_ids = set()
        collector = self.get_container()['collector']
        user_service = self.get_container()['user_service']

        dates_ranges = DateHelper.split_period([self.option('from'),
                                                self.option('to')],
                                               int(self.option('step')))
        self.line("Split to {} ranges".format(len(dates_ranges)))
        for dates_range in dates_ranges:
            self.line(" Collect {} - {} ...".format(dates_range[0], dates_range[1]))
            self.line("\n")
            user_ids |= collector.collect_referrer(dates_range, self.progress_bar())
            self.line("\n")

        self.line("Get {} user ids\n".format(len(user_ids)))
        progress = self.progress_bar(len(user_ids))
        referrer_service = self.get_container()['referrer_service']
        first_referrers = referrer_service.get_first_referrer(list(user_ids))
        for row in first_referrers:
            user_service.update_referrer(row['user_id'], row['referrer'])
            progress.advance()
        progress.finish()

        self.line("\nDone!")
