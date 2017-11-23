class Referrer(object):
    _db = None

    def __init__(self, db):
        self._db = db
        super().__init__()

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """INSERT IGNORE INTO referrer (userId, createdAt, referrer) VALUES(%s, %s, %s)"""
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))

    def get_first_referrer(self, user_ids):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                      l.userId as user_id,
                      l.referrer
                    FROM 
                      referrer AS l
                      INNER JOIN (
                        SELECT
                          userId,
                          MIN(createdAt) AS mct
                        FROM referrer
                        WHERE
                          userId IN (%s)
                        GROUP BY
                          userId
                      ) AS r
                      ON (l.userId = r.userId AND l.createdAt = r.mct);
                """
                in_p = ', '.join(list(map(lambda x: '%s', user_ids)))
                sql = sql % in_p
                cursor.execute(sql, user_ids)
                return cursor.fetchall()
        except Exception as e:
            print(str(e))
