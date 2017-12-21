class Band(object):
    _db = None

    def __init__(self, db):
        self._db = db
        super().__init__()

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    INSERT IGNORE INTO `band` (`userId`, `createdAt`, `name`, `uniqueCnt`, `totalCnt`)
                    VALUES(%s, %s, %s, %s, %s)
                """
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))

    def count_bands(self, user_ids):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                      userId,
                      DATE_FORMAT(createdAt, '%%Y-%%m') AS monthly,
                      SUM(totalCnt) AS cnt_bands
                    FROM
                      band
                    WHERE
                      userId IN ({})
                    GROUP BY
                      userId,
                      monthly
                """
                in_p = ', '.join(list(map(lambda x: '%s', user_ids)))
                sql = sql.format(in_p)
                cursor.execute(sql, user_ids)
                users_bands = dict()
                for row in cursor.fetchall():
                    user_id = int(row['userId'])
                    monthly = row['monthly']
                    if user_id in users_bands:
                        users_bands[user_id][monthly] = int(row['cnt_bands'])
                    else:
                        users_bands[user_id] = dict()
                        users_bands[user_id][monthly] = int(row['cnt_bands'])
                return users_bands
        except Exception as e:
            print(str(e))

    def total_bands_by_period(self, user_ids, period):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                      userId,
                      SUM(totalCnt) AS cnt_bands
                    FROM
                      band
                    WHERE
                      userId IN ({})
                      AND createdAt BETWEEN %s AND %s
                    GROUP BY
                      userId
                """
                in_p = ', '.join(list(map(lambda x: '%s', user_ids)))
                sql = sql.format(in_p)
                cursor.execute(sql, user_ids + [
                    '{} 00:00:00'.format(period[0]),
                    '{} 23:59:59'.format(period[1])])
                return dict((row['userId'], row['cnt_bands']) for row in cursor.fetchall())
        except Exception as e:
            print(str(e))
