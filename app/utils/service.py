import os

from pymysql import cursors, connect

from app.service.band import Band
from app.service.collector import Collector
from app.service.dowload import Download
from app.service.google_analytic import GoogleAnalytic
from app.service.language import Language
from app.service.payment import Payment
from app.service.referrer import Referrer
from app.service.report.paid_activity import PaidActivity
from app.service.report.registration_way import RegistrationWay
from app.service.report.top100 import Top100
from app.service.scene import Scene
from app.service.session import Session
from app.service.user import User
from app.utils.container import Container

container = Container()

# db parameters
container['db_host'] = os.getenv('DATABASE_HOST')
container['db_name'] = os.getenv('DATABASE_NAME')
container['db_user'] = os.getenv('DATABASE_USER')
container['db_password'] = os.getenv('DATABASE_PASSWORD')

# ga parameters
container['ga_view_id'] = os.getenv('GA_VIEW_ID')
container['ga_scopes'] = [os.getenv('GA_SCOPE')]
container['ga_key_file_location'] = os.getenv('GA_KEY_FILE_LOCATION')

# db service
container['db'] = lambda c: connect(host=c['db_host'],
                                    user=c['db_user'],
                                    password=c['db_password'],
                                    db=c['db_name'],
                                    charset='utf8',
                                    cursorclass=cursors.DictCursor)
container.share('db')

# ga service
container['ga'] = lambda c: GoogleAnalytic(view_id=c['ga_view_id'],
                                           scopes=c['ga_scopes'],
                                           key_file_location=c['ga_key_file_location'])
container.share('ga')

# data services
container['language_service'] = lambda c: Language(c['db'])
container.share('language_service')

container['user_service'] = lambda c: User(c['db'])
container.share('user_service')

container['payment_service'] = lambda c: Payment(c['db'])
container.share('payment_service')

container['scene_service'] = lambda c: Scene(c['db'])
container.share('scene_service')

container['band_service'] = lambda c: Band(c['db'])
container.share('band_service')

container['download_service'] = lambda c: Download(c['db'])
container.share('download_service')

container['referrer_service'] = lambda c: Referrer(c['db'])
container.share('referrer_service')

container['session_service'] = lambda c: Session(c['db'])
container.share('session_service')

container['collector'] = lambda c: Collector(c['ga'], c['session_service'], c['scene_service'],
                                             c['band_service'], c['download_service'],
                                             c['referrer_service'], c['language_service'])
container.share('collector')


# report services
container['top100'] = lambda c: Top100(c['db'], c['user_service'], c['payment_service'],
                                       c['band_service'], c['download_service'], c['session_service'])
container.share('top100')


container['registration_way'] = lambda c: RegistrationWay(c['db'])
container.share('registration_way')

container['paid_activity'] = lambda c: PaidActivity(c['payment_service'], c['user_service'],
                                                    c['scene_service'], c['band_service'],
                                                    c['download_service'])
container.share('paid_activity')
