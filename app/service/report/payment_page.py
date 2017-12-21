class PaymentPage(object):
    """
    A PaymentPage is the service for building report data
    """
    def __init__(self, db):
        """
        Constructor

        :param db: Db connection
        :type db: pymysql.connect
        """
        self._db = db

    def get_report(self):
        """
        Return report data group by month

        :return: report data
        :rtype: list
        """
        months = range(1, 13)
        for month in months:
            reg_stat = self._get_reg_stat(month)
            # login_stat = self._get_login_stat(month)

    def _get_reg_stat(self, month):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        COUNT(DISTINCT u.id) AS total_reg,
                        SUM(IF(pt.type = 'open_payment_page', 1, 0)) as open_pp,
                        SUM(IF(pt.type = 'open_payment_form', 1, 0)) as open_pf
                    FROM
                        user AS u LEFT JOIN payment_track AS pt ON (u.id = pt.userId)
                    WHERE
                        MONTH(u.createdAt) = %s AND MONTH(pt.createdAt) = %s
                """
                cursor.execute(sql, [month, month])
                dd = cursor.fetchone()
                return [list(row.values()) for row in cursor.fetchone()]
        except Exception as e:
            print(str(e))

    def get_report_by_week(self , period):
        """
        Return report data group by week

        :param period: Report period. For example [2017-01-01, 2017-01-31]
        :type period: list

        :return: report data
        :rtype: list
        """
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        DATE_FORMAT(createdAt, '%%Y-%%m-%%u') as monthly,
                        COUNT(*) AS total_reg,
                        SUM(IF(provider = 'facebook', 1, 0)) AS from_facebook,
                        SUM(IF(provider = 'google-oauth2', 1, 0)) AS from_google,
                        SUM(IF(provider = 'linkedin-oauth2', 1,  0)) AS from_linkedin,
                        SUM(IF(provider = 'email', 1, 0)) AS from_email,
                        SUM(IF(emailConfirm = 1 AND provider = 'email', 1, 0)) AS confirm
                    FROM
                        user
                    WHERE
                        createdAt >= %s
                        AND createdAt <= %s
                    GROUP BY
                        monthly
                """
                cursor.execute(sql, period)
                return [list(row.values()) for row in cursor.fetchall()]
        except Exception as e:
            print(str(e))

