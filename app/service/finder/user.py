class User(object):
    def __init__(self, db):
        """
        Constructor

        :param db: Db connection
        :type db: pymysql.connect
        """
        self._db = db

    def find_user_ids(self, scene_count, period):
        """
        Find user ids that view scene_count scenes in period

        :param scene_count: Scenes count
        :type scene_count: int
        :param period: Report period. For example [2017-01-01, 2017-01-31]
        :type period: list

        :return: List of user ids
        :rtype: list
        """
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        userId as user_id,
                        COUNT(DISTINCT createdAt, name) AS unique_in_period
                    FROM
                        scene
                    WHERE
                        actionWay != 'search_by_address'
                        AND createdAt BETWEEN %s AND %s
                    GROUP BY
                        user_id
                    HAVING
                        unique_in_period = %s
                """
                cursor.execute(sql, period + [scene_count])
                return [int(row['user_id']) for row in cursor.fetchall()]
        except Exception as e:
            print(str(e))

    def find_active_n_month_user_ids(self, active_month, period):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        DISTINCT t1.userId as user_id
                    FROM
                        (
                            SELECT
                                t.userId AS userId,
                                count(t.monthly) AS month_with_login
                            FROM
                                (
                                    SELECT
                                        userId,
                                        MONTH(createdAt) as monthly,
                                        COUNT(*) as loginCnt
                                    FROM
                                        session
                                    WHERE
                                        createdAt between %s AND %s
                                    GROUP BY
                                        userId,
                                        monthly
                                ) as t
                            GROUP BY
                                userId
                        ) as t1
                        LEFT JOIN language as l ON (t1.userId = l.userId)
                    WHERE
                        t1.month_with_login = %s
                        AND l.lang like 'en%%'
                """
                cursor.execute(sql, [
                    '{} 00:00:00'.format(period[0]),
                    '{} 23:59:59'.format(period[1]),
                    active_month
                ])
                return [int(row['user_id']) for row in cursor.fetchall()]
        except Exception as e:
            print(str(e))
