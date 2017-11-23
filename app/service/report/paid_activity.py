from datetime import datetime


class PaidActivity(object):
    """
    A PaidActivity is the service for building report data
    """

    def __init__(self,
                 payment_service,
                 user_service,
                 scene_service,
                 band_service,
                 download_service):
        """
        Constructor

        :param payment_service: The payment service
        :type payment_service: app.service.payment.Payment
        :param user_service: The user service
        :type user_service: app.service.user.User
        :param scene_service: The scene service
        :type scene_service: app.service.scene.Scene
        :param band_service: The band service
        :type band_service: app.service.band.Band
        :param download_service: The download service
        :type download_service: app.service.download.Download
        """
        self._payment_service = payment_service
        self._user_service = user_service
        self._scene_service = scene_service
        self._band_service = band_service
        self._download_service = download_service

    def get_report(self):
        """
        Return report data - list of lists

        :return: report data
        :rtype: list
        """
        # get first payments
        first_payments = self._payment_service.get_first_payments()
        user_ids = list(first_payments.keys())
        # get user base information
        users_info = self._user_service.get_users(user_ids)
        # get user scenes view group by month
        users_scenes = self._scene_service.count_scenes(user_ids)
        # get user bands group by month
        users_bands = self._band_service.count_bands(user_ids)
        # get user downloads group by month
        users_downloads = self._download_service.count_downloads(user_ids)

        result = []
        empty_row = ['', '', '', '', '', '', '', '', '']
        for user_id, user in users_info.items():
            print(user_id)
            row = [
                user.get('id'),  # userId
                user.get('email'),  # email
                user.get('country'),  # country
                user.get('industry'),  # industry
                user.get('website'),  # website
                ', '.join([i for i in user.get('social').split(',') if i]),  # social
                user.get('createdAt').strftime('%Y-%m-%d'),
                first_payments.get(user_id).strftime('%Y-%m-%d'),
                user.get('referrer')
            ]

            after_reg, after_pay = self._collect_scenes_bands_downloads(
                user.get('createdAt').date(),
                first_payments.get(user_id),
                dict(
                    scenes=users_scenes.get(user_id),
                    bands=users_bands.get(user_id),
                    downloads=users_downloads.get(user_id)
                )
            )
            row_cnt = max(len(after_pay), len(after_reg))

            self._add_if_exists(row, after_reg, 0)
            self._add_if_exists(row, after_pay, 0)
            result.append(row)
            for i in range(1, row_cnt):
                row = [] + empty_row
                self._add_if_exists(row, after_reg, i)
                self._add_if_exists(row, after_pay, i)
                result.append(row)

    @staticmethod
    def _add_if_exists(row, item, index):
        """
        Append data to row if item exist

        :param row: A row of data set
        :type row: list
        :param item: A list of inserted data
        :type item: list
        :param index: index that will be added to row
        :type index: basestring

        :return: A row with added item
        :rtype: list
        """
        try:
            row.append(item[index][0])
            row.append(item[index][1])
        except IndexError:
            row.append('')
            row.append('')
        return row

    def _collect_scenes_bands_downloads(self, reg_date, pay_date, data):
        """
        Group by scenes, bands, downloads data to report format

        :param reg_date: Date of registration
        :type reg_date: datetime.date
        :param pay_date: Date of payment
        :type pay_date: datetime.date
        :param data: Dictionary that contain scenes, bands, downloads data
        :type data: dict
        :return: List of data after registration data, List of data after payment data
        :rtype: list, list
        """
        scenes_reg, scenes_pay = self._format(reg_date, pay_date, data.get('scenes'))
        bands_reg, bands_pay = self._format(reg_date, pay_date, data.get('bands'))
        downloads_reg, downloads_pay = self._format(reg_date, pay_date, data.get('downloads'))

        after_reg = dict()
        after_pay = dict()

        for orderly_month, scenes in scenes_reg.items():
            after_reg[orderly_month] = dict(scenes=scenes)
        for orderly_month, scenes in scenes_pay.items():
            after_pay[orderly_month] = dict(scenes=scenes)
        for orderly_month, bands in bands_reg.items():
            if orderly_month in after_reg:
                after_reg[orderly_month]['bands'] = bands
            else:
                after_reg[orderly_month] = dict(bands=bands)
        for orderly_month, bands in bands_pay.items():
            if orderly_month in after_pay:
                after_pay[orderly_month]['bands'] = bands
            else:
                after_pay[orderly_month] = dict(bands=bands)
        for orderly_month, downloads in downloads_reg.items():
            if orderly_month in after_reg:
                after_reg[orderly_month]['downloads'] = downloads
            else:
                after_reg[orderly_month] = dict(downloads=downloads)
        for orderly_month, downloads in downloads_pay.items():
            if orderly_month in after_pay:
                after_pay[orderly_month]['downloads'] = downloads
            else:
                after_pay[orderly_month] = dict(downloads=downloads)

        after_reg_plain = list()
        for month_number, month_data in after_reg.items():
            for metric, metric_data in month_data.items():
                metric_month = list(metric_data.keys())[0]
                metric_value = list(metric_data.values())[0]
                after_reg_plain.append(
                    ("Month {} after reg ({}), {}".format(month_number, metric, metric_month), metric_value))

        after_pay_plain = list()
        for month_number, month_data in after_pay.items():
            for metric, metric_data in month_data.items():
                metric_month = list(metric_data.keys())[0]
                metric_value = list(metric_data.values())[0]
                after_pay_plain.append(
                    ("Month {} after Payment ({}), {}".format(month_number, metric, metric_month), metric_value))
        return after_reg_plain, after_pay_plain

    def _format(self, reg_date, pay_date, data):
        """
        Return after_reg and after_pay data

        :param reg_date: Date of registration
        :type reg_date: datetime.date
        :param pay_date: Date of payment
        :type pay_date: datetime.date
        :param data: Dictionary like {month => cnt}
        :type data: dict

        :return: Dictionary with after registration info, Dictionary with after payment info
        :rtype: dict, dict
        """
        if not data:
            return dict(), dict()

        after_reg = dict()
        after_pay = dict()

        for month, cnt in data.items():
            month_dt = datetime.strptime(month, '%Y-%m').date()
            if month_dt > pay_date:  # after_pay
                orderly_month = self._diff_month(month_dt, pay_date)
                after_pay[orderly_month] = dict([(month, cnt)])
            else:  # after reg
                orderly_month = self._diff_month(month_dt, reg_date)
                after_reg[orderly_month] = dict([(month, cnt)])
        return after_reg, after_pay

    @staticmethod
    def _diff_month(d1, d2):
        """
        Return count days between two dates

        :param d1: First date
        :type d1: datetime.date
        :param d2: Second date
        :type d2: datetime.date

        :return: Count days between two dates
        :rtype: int
        """
        return (d1.year - d2.year) * 12 + d1.month - d2.month
