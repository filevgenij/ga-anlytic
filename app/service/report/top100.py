from datetime import datetime


class Top100(object):
    """
    A Top100 is the service for building report data
    """

    _user_service = None
    _payment_service = None
    _band_service = None
    _download_service = None
    _session_service = None
    _db = None

    def __init__(self,
                 db,
                 user_service,
                 payment_service,
                 band_service,
                 download_service,
                 session_service):
        """
        Constructor

        :param db: Db connection
        :type db: pymysql.connect
        :param user_service: The user service
        :type user_service: app.service.user.User
        :param payment_service: The payment service
        :type payment_service: app.service.payment.Payment
        :param band_service: The band service
        :type band_service: app.service.band.Band
        :param download_service: The download service
        :type download_service: app.service.download.Download
        :param session_service: The session service
        :type session_service: app.service.session.Session
        """
        self._user_service = user_service
        self._payment_service = payment_service
        self._band_service = band_service
        self._download_service = download_service
        self._session_service = session_service
        self._db = db

    def get_report(self, period, language):
        """
        Return report data according input params

        :param period: Report period. For example [2017-01-01, 2017-01-31]
        :type period: list
        :param language: Language for filtering report data. "all" value will disable filtering
        :type language: basestring
        :return: List of report data
        :rtype: list
        """
        top100 = self._get_top100_user_ids(period, language)
        user_ids = list(top100.keys())

        users_info = self._user_service.get_users(user_ids)
        first_payments = self._payment_service.get_first_payments()
        total_bands = self._band_service.total_bands_by_period(user_ids, period)
        total_downloads = self._download_service.total_downloads_by_period(user_ids, period)
        days_with_login = self._session_service.get_days_with_login(user_ids, period)

        data = []
        for user_id, row in top100.items():
            data.append([
                user_id,
                users_info.get(user_id).get('email'),
                users_info.get(user_id).get('country'),
                users_info.get(user_id).get('industry'),
                users_info.get(user_id).get('website'),
                ', '.join([i for i in users_info.get(user_id).get('social').split(',') if i]),
                users_info.get(user_id).get('createdAt').strftime('%Y-%m-%d'),
                first_payments.get(user_id).strftime('%Y-%m-%d') if user_id in first_payments else '',
                row.get('unique_scenes'),
                total_bands.get(user_id),
                total_downloads.get(user_id),
                (datetime.now().date() - users_info.get(user_id).get('createdAt')).days,
                days_with_login.get(user_id).get('days_with_login'),
                days_with_login.get(user_id).get('days_in_period'),
                row.get('language')
            ])
        return data

    def _get_top100_user_ids(self, period, language):
        """
        Return top 100 user_ids, their languages and amount of unique scenes

        :param period: Report period. For example [2017-01-01, 2017-01-31]
        :type period: list
        :param language: Language for filtering report data. "all" value will disable filtering
        :type language: str

        :return: Dictionary like dict(user_id => user_data_dictionary,...)
        :rtype: dict
        """
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        u.id as user_id,
                        COUNT(DISTINCT s.createdAt, s.name) AS unique_scenes,
                        GROUP_CONCAT(DISTINCT l.lang) AS language
                    FROM
                        user AS u
                        INNER JOIN scene AS s ON (u.id = s.userId)
                        LEFT JOIN language AS l ON (u.id = l.userId)
                    WHERE
                        s.createdAt BETWEEN %s AND %s
                        AND l.lang != '(not set)'
                        AND s.actionWay != 'search_by_address'
                        %s
                    GROUP BY
                        u.id
                    ORDER BY
                        unique_scenes DESC
                    LIMIT 100
                """
                lang_condition = "AND l.lang LIKE '{}%".format(language) if language != 'all' else ""
                cursor.execute(sql, ['{} 00:00:00'.format(period[0]),
                                     '{} 23:59:59'.format(period[1]),
                                     lang_condition])
                return dict((row['user_id'], row) for row in cursor.fetchall())
        except Exception as e:
            print(str(e))

