from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadPaymentTrackCommand(BaseCommand):
    """
    Load payments track from csv file (userId, type, createdAt).

    csv:load:payment_track
        {--path= : Path to csv file. Set absolute path.}
    """

    def handle(self):
        path = self.option('path')

        payment_track_service = self.get_container()['payment_track_service']
        data = CsvReader.get_reader(path)

        progress = self.progress_bar()
        for row in data:
            payment_track_service.insert(list(row.values()))
            progress.advance()

        progress.finish()
        self.line("\nDone!")

# SELECT
#     actor_object_id AS user_id,
#     verb AS type,
#     to_char(timestamp, 'YYYY-MM-DD HH24:MI:SS') AS createdAt
# FROM
#     actstream_action
# WHERE
#     verb IN ('open_payment_page', 'open_payment_form');

