from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadUserIpCommand(BaseCommand):
    """
    Load user ip from csv (ip, user_id) and append it to user data

    csv:load:user_ip
        {--path= : Path to csv file. Set absolute path}
    """
    def handle(self):
        user_service = self.get_container()['user_service']
        reader = CsvReader.get_reader(self.option('path'))

        progress = self.progress_bar()
        for row in reader:
            if not row['user_id'].isnumeric():
                progress.advance()
                continue

            user_service.update_ip(int(row['user_id']), row['ip'])
            progress.advance()

        progress.finish()
        self.line("\nDone!")
