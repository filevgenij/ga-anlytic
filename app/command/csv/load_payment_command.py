from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadPaymentsCommand(BaseCommand):
    """
    Load payments from csv file (userId, paymentDate, typeOfPayment).

    csv:load:payment
        {--path= : Path to csv file. Set absolute path.}
    """

    def handle(self):
        path = self.option('path')

        payment_service = self.get_container()['payment_service']
        data = CsvReader.get_reader(path)

        progress = self.progress_bar()
        for row in data:
            payment_service.insert(list(row.values()))
            progress.advance()

        progress.finish()
        self.line("\nDone!")


# Query for build csv file
# SELECT
#     ip,
#     s.user_id
# FROM
#     tracking_registration
