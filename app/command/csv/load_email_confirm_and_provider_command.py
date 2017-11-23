from app.utils.base_command import BaseCommand
from app.utils.hepler.csv import CsvReader


class LoadEmailConfirmAndProviderCommand(BaseCommand):
    """
    Load email confirm data and social provider from csv (user_id, confirm, provider) and append it to user data

    csv:load:email_confirm_and_provider
        {--path= : Path to csv file. Set absolute path}
    """
    def handle(self):
        user_service = self.get_container()['user_service']
        reader = CsvReader.get_reader(self.option('path'))

        progress = self.progress_bar()
        progress.set_redraw_frequency(100)
        for row in reader:
            if not row['user_id'].isnumeric():
                progress.advance()
                continue

            user_service.update_email_confirm_and_provider(
                int(row['user_id']),
                1 if row['email_confirmed'] == 'True' else 0,
                row['provider'] if row['provider'] != '' else 'email'
            )
            progress.advance()

        progress.finish()
        self.line("\nDone!")


# SELECT
#     c.user_id,
#     c.verified AS email_confirmed,
#     s.provider
# FROM
#     account_emailconfirm AS c
#     LEFT JOIN social_auth_usersocialauth AS s ON (c.user_id = s.user_id)
# ORDER by 1
