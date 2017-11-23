from datetime import datetime

from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadUserFullNameCommand(BaseCommand):
    """
    Load users fullname from csv file.

    csv:load:user_fullname
        {--path= : Path to csv file. Set absolute path}
    """

    def handle(self):
        user_service = self.get_container()['user_service']
        reader = CsvReader.get_reader(self.option('path'))

        progress = self.progress_bar()
        progress.set_redraw_frequency(100)
        for row in reader:
            if not row['id'].isnumeric():
                progress.advance()
                continue

            user_service.update_fullname(int(row['id']), row['first_name'], row['last_name'])
            progress.advance()

        progress.finish()
        self.line("\nDone!")
