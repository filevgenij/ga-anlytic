from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadReferrerUrlCommand(BaseCommand):
    """
    Load referrer urls from csv file (userId, url).

    csv:load:referrer_url
        {--path= : Path to csv file. Set absolute path.}
    """

    def handle(self):
        path = self.option('path')

        referrer_url_service = self.get_container()['referrer_url_service']
        data = CsvReader.get_reader(path)

        progress = self.progress_bar()
        for row in data:
            referrer_url_service.insert(list(row.values()))
            progress.advance()

        progress.finish()
        self.line("\nDone!")

# SELECT
#     tr.user_id as user_id,
#     tv.url
# FROM
#     tracking_registration as tr
#     INNER JOIN tracking_visiturl as tv ON (tr.last_visit_url_id = tv.id)
# WHERE
#     tr.last_visit_date > '2017-09-11 00:00:00' AND tr.last_visit_date < '2017-12-11 23:59:59'

