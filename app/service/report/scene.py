import calendar
from datetime import datetime, timedelta
from itertools import zip_longest


class Scene(object):
    """
    A Scene is the service for building report data for scene report
    """

    def __init__(self, db):
        """
        Constructor

        :param db: Db connection
        :type db: pymysql.connect
        """
        self._db = db

    def get_report(self, scene_metrics, only_paid_search):
        """
        Return report data according input params

        :param scene_metrics: Tuple of scene metric. The item can be scalar value or tuple with two items
        :type scene_metrics: tuple
        :param only_paid_search: Calculate only paid users
        :type only_paid_search: bool

        :return: List of report data
        :rtype: list
        """

        data = []
        for metric in scene_metrics:
            if isinstance(metric, tuple):
                row = list(self._get_users_by_scene_range(metric, only_paid_search).values())
                row.insert(0, '{} - {}'.format(metric[0], metric[1]))
            elif metric == 0:
                row = self._get_users_without_scenes(only_paid_search)
                row.insert(0, '0')
            else:
                row = list(self._get_users_by_scene_scalar(metric, only_paid_search).values())
                row.insert(0, metric)
            data.append(row)

        return data

    def _get_users_by_scene_scalar(self, metric, only_paid_search=False):
        return self._get_users_by_scene_range((metric, metric), only_paid_search)

    def _get_users_by_scene_range(self, metric, only_paid_search=False):
        from_, to_ = metric
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        SUM(IF(t.monthly = 5, 1, 0)) as May,
                        SUM(IF(t.monthly = 6, 1, 0)) as June,
                        SUM(IF(t.monthly = 7, 1, 0)) as July,
                        SUM(IF(t.monthly = 8, 1, 0)) as August,
                        SUM(IF(t.monthly = 9, 1, 0)) as September,
                        SUM(IF(t.monthly = 10, 1, 0)) as October,
                        SUM(IF(t.monthly = 11, 1, 0)) as November,
                        SUM(IF(t.monthly = 12, 1, 0)) as December
                    FROM
                        (SELECT
                            s.userId,
                            MONTH(s.createdAt) AS monthly,
                            COUNT(DISTINCT s.createdAt, s.name) AS unique_in_month
                        FROM
                            scene AS s
                """
                if only_paid_search:
                    sql += ' INNER JOIN user AS u ON (s.userId = u.id) '
                sql += """
                    WHERE
                        s.actionWay != 'search_by_address'
                        AND MONTH(s.createdAt) BETWEEN 5 AND 12
                """
                if only_paid_search:
                    sql += " AND u.trafficSource = 'Paid Search' "
                sql += """
                        GROUP BY
                            userId,
                            monthly
                        ) AS t
                    WHERE
                        t.unique_in_month BETWEEN %s AND %s
                """
                cursor.execute(sql, [from_, to_])
                return cursor.fetchone()
        except Exception as e:
            print(str(e))

    def _get_users_without_scenes(self, only_paid_search):
        data = []
        for month in range(5, 13):
            row = self._get_users_without_scenes_in_month(only_paid_search, month)
            sba_only = row['totalUsersWhoViewsSBAOnly'] if row['totalUsersWhoViewsSBAOnly'] is not None else 0
            login_only = row['onlyLogin'] if row['onlyLogin'] is not None else 0
            data.append(sba_only + login_only)
        return data

    def _get_users_without_scenes_in_month(self, only_paid_search, month):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                        SUM(IF(t.other > 0, 1, 0)) AS totalUsersView,
                        SUM(IF(t.other = 0 AND t.search_by_address > 0, 1, 0)) AS totalUsersWhoViewsSBAOnly,
                        SUM(IF(t.onlyLogin > 0, 1, 0)) AS onlyLogin
                    FROM 
                        (
                            SELECT
                                t_sessions.userId,
                                t_scenes.search_by_address,
                                t_scenes.other,
                                SUM(IF(t_scenes.userId IS NULL, 1, 0)) AS onlyLogin
                            FROM
                                ( """ + self._get_session_query(only_paid_search) + """ ) AS t_sessions
                                LEFT JOIN
                                ( """ + self._get_scene_query(only_paid_search) + """ ) AS t_scenes ON (t_sessions.userId = t_scenes.userId)
                            GROUP BY
                                t_sessions.userId
                        ) as t;
                """
                cursor.execute(sql, [month, month])
                return cursor.fetchone()
        except Exception as e:
            print(str(e))



    @staticmethod
    def _get_session_query(only_paid_search):
        sql = """
            SELECT
                s.userId,
                COUNT(*) AS sessionCnt
            FROM
                session AS s
        """
        if only_paid_search:
            sql += " INNER JOIN user AS u ON (s.userId = u.id) "

        sql += """
            WHERE
                month(s.createdAt) = %s
        """

        if only_paid_search:
            sql += "AND u.trafficSource = 'Paid Search' "

        sql += """
            GROUP BY
                userId
        """

        return sql

    @staticmethod
    def _get_scene_query(only_paid_search):
        sql = """
            SELECT
                s.userId,
                SUM(IF(s.actionWay='search_by_address', 1, 0)) AS search_by_address,
                SUM(IF(s.actionWay != 'search_by_address', 1, 0)) AS other
            FROM
                scene AS s
        """

        if only_paid_search:
            sql += " INNER JOIN user AS u ON (s.userId = u.id) "

        sql += """
            WHERE
                month(s.createdAt) = %s
        """

        if only_paid_search:
            sql += "AND u.trafficSource = 'Paid Search' "

        sql += """
            GROUP BY
                userId
        """

        return sql

