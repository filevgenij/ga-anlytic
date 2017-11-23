from datetime import datetime

from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadUserCommand(BaseCommand):
    """
    Load users from csv file. Duplicates are ignored.

    csv:load:user
        {--path= : Path to csv file. Set absolute path}
    """

    def handle(self):
        user_service = self.get_container()['user_service']
        reader = CsvReader.get_reader(self.option('path'))

        progress = self.progress_bar()
        for row in reader:
            if not row['id'].isnumeric():
                progress.advance()
                continue

            social = [row[s] for s in ['facebook', 'google-oauth2', 'linkedin-oauth2'] if row[s]]

            user_service.insert([
                int(row['id']),
                row['email'],
                row['country'],
                row['industry'],
                row['website'],
                ', '.join(social),
                datetime.strptime(row['date_joined'], '%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%d'),
                row['first_name'],
                row['last_name']
            ])
            progress.advance()

        progress.finish()
        self.line("\nDone!")
