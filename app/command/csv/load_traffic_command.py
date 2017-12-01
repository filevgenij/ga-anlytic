from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadTrafficCommand(BaseCommand):
    """
    Load user traffic data from csv (ip, user_id) and append it to user data

    csv:load:traffic
        {--path= : Path to csv file. Set absolute path}
    """
    def handle(self):
        user_service = self.get_container()['user_service']
        reader = CsvReader.get_reader(self.option('path'))

        traffic_source = 'Paid Search'
        search_pattern = 'utm_source=google_as'
        progress = self.progress_bar()
        for row in reader:
            if not row['user_id'].isnumeric() or row['url'].find(search_pattern) == -1:
                progress.advance()
                continue

            user_service.update_traffic_source(int(row['user_id']), traffic_source)
            progress.advance()

        progress.finish()
        self.line("\nDone!")
