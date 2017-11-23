from app.utils.base_command import BaseCommand
from app.utils.hepler.date import DateHelper


class LoadAllCommand(BaseCommand):
    """
    Load all data(session, scene, band, download, referrer, language) from GA

    ga:load:all
        {--from= : Date from in format YYYY-MM-DD}
        {--to= : Date to in format YYYY-MM-DD}
        {--step=2: Step for date range}
    """
    def handle(self):
        user_ids = set()
        collector = self.get_container()['collector']
        dates_ranges = DateHelper.split_period([self.option('from'),
                                                self.option('to')],
                                               int(self.option('step')))
        self.line("Amount of periods - {}".format(len(dates_ranges)))
        for dates_range in dates_ranges:
            self.line("\nPeriod => {} - {}".format(dates_range[0], dates_range[1]))
            # collect sessions
            self.line("\nCollect sessions...")
            collector.collect_session(dates_range, self.progress_bar())
            # collect scenes
            self.line("\nCollect scenes...")
            collector.collect_scene(dates_range, self.progress_bar())
            # collect bands
            self.line("\nCollect bands...")
            collector.collect_band(dates_range, self.progress_bar())
            # collect downloads
            self.line("\nCollect downloads...")
            collector.collect_download(dates_range, self.progress_bar())
            # collect languages
            self.line("\nCollect languages...")
            collector.collect_language(dates_range, self.progress_bar())
            # collect referrers
            self.line("\nCollect referrers...")
            user_ids |= collector.collect_referrer(dates_range, self.progress_bar())

        self.line("\nGet {} user ids from referrer data".format(len(user_ids)))
        progress = self.progress_bar(len(user_ids))
        referrer_service = self.get_container()['referrer_service']
        first_referrers = referrer_service.get_first_referrer(list(user_ids))
        user_service = self.get_container()['user_service']
        for row in first_referrers:
            user_service.update_referrer(row['user_id'], row['referrer'])
            progress.advance()
        progress.finish()

        self.line("\nDone!")
