class Scene(object):
    _db = None

    def __init__(self, db):
        self._db = db
        super().__init__()

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    INSERT IGNORE INTO `scene` (`userId`, `createdAt`, `actionWay`, `name`, `uniqueCnt`, `totalCnt`)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))

    def count_scenes(self, user_ids):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    SELECT
                      userId,
                      DATE_FORMAT(createdAt, '%%Y-%%m') AS monthly,
                      COUNT(DISTINCT createdAt, name) AS cnt_scenes
                    FROM
                      scene
                    WHERE
                      userId IN ({})
                      AND actionWay != 'search_by_address'
                    GROUP BY
                      userId,
                      monthly
                """
                in_p = ', '.join(list(map(lambda x: '%s', user_ids)))
                sql = sql.format(in_p)
                cursor.execute(sql, user_ids)
                user_info = dict()
                for row in cursor.fetchall():
                    user_id = int(row['userId'])
                    monthly = row['monthly']
                    if user_id in user_info:
                        user_info[user_id][monthly] = int(row['cnt_scenes'])
                    else:
                        user_info[user_id] = dict()
                        user_info[user_id][monthly] = int(row['cnt_scenes'])
                return user_info
        except Exception as e:
            print(str(e))

