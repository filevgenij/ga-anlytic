from cleo import Application

from app.command.csv.load_email_confirm_and_provider_command import LoadEmailConfirmAndProviderCommand
from app.command.csv.load_payment_command import LoadPaymentsCommand
from app.command.csv.load_payment_track_command import LoadPaymentTrackCommand
from app.command.csv.load_referrer_url_command import LoadReferrerUrlCommand
from app.command.csv.load_user_command import LoadUserCommand
from app.command.csv.load_user_fullname import LoadUserFullNameCommand
from app.command.csv.load_user_ip_command import LoadUserIpCommand
from app.command.csv.load_traffic_command import LoadTrafficCommand as CsvLoadTrafficCommand
from app.command.ga.load_all_command import LoadAllCommand
from app.command.ga.load_band_command import LoadBandCommand
from app.command.ga.load_download_command import LoadDownloadCommand
from app.command.ga.load_language_command import LoadLanguageCommand
from app.command.ga.load_referrer_command import LoadReferrerCommand
from app.command.ga.load_scene_command import LoadSceneCommand
from app.command.ga.load_session_command import LoadSessionCommand
from app.command.ga.load_traffic_command import LoadTrafficCommand as GaLoadTrafficCommand
from app.command.report.paid_activity_command import PaidActivityCommand
from app.command.report.payment_page_command import PaymentPageCommand
from app.command.report.registration_way_command import RegistrationWayCommand
from app.command.report.retention_command import RetentionCommand
from app.command.report.scenes_command import SceneCommand
from app.command.report.top_100_command import Top100Command
from app.command.report.user_info_select_by_active_months_command import UserInfoSelectByActiveMonthsCommand
from app.command.report.user_info_select_by_scene_command import UserInfoSelectBySceneCommand
from app.utils.base_command import BaseCommand
from app.utils.service import container

BaseCommand.container = container

application = Application()

# cvs commands
application.add(LoadPaymentsCommand())
application.add(LoadPaymentTrackCommand())
application.add(LoadUserCommand())
application.add(LoadUserIpCommand())
application.add(LoadEmailConfirmAndProviderCommand())
application.add(LoadUserFullNameCommand())
application.add(CsvLoadTrafficCommand())
application.add(LoadReferrerUrlCommand())

# ga commands
application.add(LoadBandCommand())
application.add(LoadReferrerCommand())
application.add(LoadSceneCommand())
application.add(LoadDownloadCommand())
application.add(LoadSessionCommand())
application.add(LoadLanguageCommand())
application.add(LoadAllCommand())
application.add(GaLoadTrafficCommand())

# report commands
application.add(PaidActivityCommand())
application.add(Top100Command())
application.add(RegistrationWayCommand())
application.add(UserInfoSelectBySceneCommand())
application.add(UserInfoSelectByActiveMonthsCommand())
application.add(RetentionCommand())
application.add(SceneCommand())
application.add(PaymentPageCommand())

if __name__ == '__main__':
    application.run()