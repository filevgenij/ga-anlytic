class ReferrerUrl(object):
    def __init__(self, db):
        self._db = db
        super().__init__()

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """INSERT IGNORE INTO referrer_url (userId, url) VALUES(%s, %s)"""
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))
