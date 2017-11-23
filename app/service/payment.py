class Payment(object):
    _db = None

    def __init__(self, db):
        self._db = db
        super().__init__()

    def insert(self, row):
        try:
            with self._db.cursor() as cursor:
                sql = """INSERT IGNORE INTO payments (userId, paymentDate, typeOfPayment) VALUES(%s, %s, %s)"""
                cursor._defer_warnings = True
                cursor.execute(sql, row)
            self._db.commit()
        except Exception as e:
            print(str(e))

    def get_first_payments(self):
        try:
            with self._db.cursor() as cursor:
                sql = """
                  SELECT
                    userId,
                    DATE(paymentDate) as paymentDate
                  FROM
                    payments
                  WHERE
                    typeOfPayment = 'order.completed'
                  ORDER BY paymentDate
                """
                cursor.execute(sql)
                return dict((row['userId'], row['paymentDate']) for row in cursor.fetchall())
        except Exception as e:
            print(str(e))
