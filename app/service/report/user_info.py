from datetime import datetime


class UserInfo(object):
    """
    An User Info is the service for building report data
    """
    def __init__(self,
                 user_service,
                 payment_service,
                 session_service,
                 scene_service,
                 band_service,
                 download_service):
        """
        Constructor

        :param user_service: The user service
        :type user_service: app.service.user.User
        :param payment_service: The payment service
        :type payment_service: app.service.payment.Payment
        :param session_service: The session service
        :type session_service: app.service.session.Session
        """
        self._user_service = user_service
        self._payment_service = payment_service
        self._session_service = session_service
        self._scene_service = scene_service
        self._band_service = band_service
        self._download_service = download_service

    def get_report(self, user_ids, period):
        """
        Return report data according input params

        :param user_ids: List of user ids
        :type user_ids: list
        :param period: Report period. For example [2017-01-01, 2017-01-31]
        :type period: list
        :return: List of report data
        :rtype: list
        """

        users_info = self._user_service.get_users(user_ids)
        first_payments = self._payment_service.get_first_payments()
        total_scenes = self._scene_service.total_scenes_by_period(user_ids, period)
        total_bands = self._band_service.total_bands_by_period(user_ids, period)
        total_downloads = self._download_service.total_downloads_by_period(user_ids, period)
        days_with_login = self._session_service.get_days_with_login(user_ids, period)

        data = []
        for user_id in user_ids:
            data.append([
                user_id,
                users_info.get(user_id).get('email'),
                "{} {}".format(users_info.get(user_id).get('firstName'), users_info.get(user_id).get('lastName')),
                users_info.get(user_id).get('country'),
                users_info.get(user_id).get('industry'),
                users_info.get(user_id).get('website'),
                ', '.join([i for i in users_info.get(user_id).get('social').split(',') if i]),
                users_info.get(user_id).get('createdAt').strftime('%Y-%m-%d'),
                first_payments.get(user_id).strftime('%Y-%m-%d') if user_id in first_payments else '',
                total_scenes.get(user_id),
                total_bands.get(user_id),
                total_downloads.get(user_id),
                (datetime.now().date() - users_info.get(user_id).get('createdAt')).days,
                days_with_login.get(user_id).get('days_with_login'),
                days_with_login.get(user_id).get('days_in_period')
            ])
        return data
