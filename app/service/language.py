class Language:
    _db = None

    def __init__(self, db):
        self._db = db
        super().__init__()

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    INSERT IGNORE INTO `language` (`userId`, `lang`)
                    VALUES (%s, %s)
                """
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))

    def get_by_user_id(self, user_ids):
        with self._db.cursor() as cursor:
            sql = 'SELECT userId, lang FROM language WHERE userId IN (%s)'
            in_p = ', '.join(list(map(lambda x: '%s', user_ids)))
            sql = sql % in_p
            cursor.execute(sql, user_ids)
            return dict((int(row['userId']), row['lang']) for row in cursor.fetchall())
