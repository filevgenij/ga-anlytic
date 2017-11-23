class User(object):
    _db = None

    def __init__(self, db):
        self._db = db
        super().__init__()

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """
                    INSERT IGNORE INTO user (id, email, country, industry, website, social, createdAt)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))

    def get_users(self, user_ids):
        try:
            with self._db.cursor() as cursor:
                sql = "SELECT * FROM user WHERE id IN (%s)"
                in_p = ', '.join(list(map(lambda x: '%s', user_ids)))
                sql = sql % in_p
                cursor.execute(sql, user_ids)
                return dict((int(row['id']), row) for row in cursor.fetchall())
        except Exception as e:
            print(str(e))

    def update_ip(self, user_id, ip):
        try:
            with self._db.cursor() as cursor:
                sql = "UPDATE user SET ip = %s WHERE id = %s"
                cursor.execute(sql, [ip, user_id])
            self._db.commit()
        except Exception as e:
            print(str(e))

    def update_referrer(self, user_id, referrer):
        try:
            with self._db.cursor() as cursor:
                sql = "UPDATE user SET referrer = %s WHERE id = %s"
                cursor.execute(sql, [referrer, user_id])
            self._db.commit()
        except Exception as e:
            print(str(e))

    def update_email_confirm_and_provider(self, user_id, email_confirm, provider):
        """
        Update email confirmation flag and registration provider.

        :param user_id: User Id
        :type user_id: int
        :param email_confirm: Email confirmation flag. "1" for confirmed users, "0" for non confirmed users
        :type email_confirm: int
        :param provider: Registration provider
        :type provider: basestring
        """
        try:
            with self._db.cursor() as cursor:
                sql = "UPDATE user SET emailConfirm = %s, provider = %s WHERE id = %s"
                cursor.execute(sql, [email_confirm, provider, user_id])
            self._db.commit()
        except Exception as e:
            print(str(e))


