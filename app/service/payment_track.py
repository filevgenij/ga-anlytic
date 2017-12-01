class PaymentTrack(object):

    def __init__(self, db):
        self._db = db

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    INSERT IGNORE INTO `payment_track` (`userId`, `type`, `createdAt`)
                    VALUES (%s, %s, %s)
                """
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))

#    def get_days_with_login(self, user_ids, period):
#        try:
#            with self._db.cursor() as cursor:
#                sql = """
#                    SELECT
#                      userId,
#                      COUNT(*) AS days_with_login,
#                      SUM(IF(createdAt BETWEEN %s AND %s, 1, 0)) AS days_in_period
#                    FROM
#                      session
#                    WHERE
#                      userId IN ({})
#                    GROUP BY
#                      userId
#                """
#                in_p = ', '.join(list(map(lambda x: '%s', user_ids)))
#                sql = sql.format(in_p)
#                cursor.execute(sql,
#                               ['{} 00:00:00'.format(period[0]), '{} 23:59:59'.format(period[1])] + user_ids)
#                return dict((row['userId'], row) for row in cursor.fetchall())
#        except Exception as e:
#            print(str(e))