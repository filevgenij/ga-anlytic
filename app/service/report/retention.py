import calendar
from datetime import datetime, timedelta
from itertools import zip_longest


class Retention(object):
    """
    A Retention is the service for building report data for retention report
    """

    def __init__(self, db):
        """
        Constructor

        :param db: Db connection
        :type db: pymysql.connect
        """
        self._db = db

    def get_report(self, only_paid_search):
        """
        Return report data according input params

        :param only_paid_search: Calculate only paid users
        :type only_paid_search: bool

        :return: List of report data
        :rtype: list
        """

        regs = self._get_registration(only_paid_search)
        pivot_data = []
        empty_col = dict((i, 0) for i in range(1,13))
        for month, reg_cnt in regs.items():
            from_, to_ = self._get_period_from_month(month)
            logins = self._get_retention_by_period(from_, to_, only_paid_search)
            column = empty_col.copy()
            column.update(logins)
            pivot_data.append([reg_cnt] + list(column.values()))

        data = list(map(list, zip_longest(*pivot_data)))

        return data

    def _get_retention_by_period(self, from_, to_, only_paid_search):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        MONTH(s.createdAt) AS monthly,
                        COUNT(DISTINCT s.userId) AS users
                    FROM
                        (SELECT 
                            id as userId,
                            createdAt,
                            trafficSource
                        FROM
                            user
                        WHERE
                            createdAt BETWEEN %s AND %s
                        ) AS regs
                        INNER JOIN session AS s ON regs.userId = s.userId
                    WHERE
                        DATE(regs.createdAt) != DATE(s.createdAt)
                """
                if only_paid_search:
                    sql += " AND regs.trafficSource = 'Paid Search'"

                sql += """
                    GROUP BY
                        monthly
                    HAVING monthly >= %s
                    ORDER BY
                        monthly asc
                    ;
                """
                cursor.execute(sql, [from_, to_, from_.month])

                return dict((row['monthly'], row['users']) for row in cursor.fetchall())
        except Exception as e:
            print(str(e))

    def _get_registration(self, only_paid_search):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        MONTH(createdAt) AS monthly,
                        COUNT(id) AS users
                    FROM
                        user
                    WHERE
                        createdAt > '2017-01-01 00:00:00'
                """
                if only_paid_search:
                    sql += " AND trafficSource = 'Paid Search' "

                sql += """
                    GROUP BY
                        monthly
                    ORDER BY
                        monthly asc
                    ;
                """
                cursor.execute(sql)
                return dict((row['monthly'], row['users']) for row in cursor.fetchall())
        except Exception as e:
            print(str(e))

    @staticmethod
    def _get_period_from_month(month):
        from_ = datetime.strptime('2017-{}-01'.format(month), '%Y-%m-%d')
        days = calendar.monthrange(from_.year, from_.month)[1]
        to_ = (from_ + timedelta(days=days)) - timedelta(seconds=1)
        return from_, to_
