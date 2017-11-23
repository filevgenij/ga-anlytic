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


