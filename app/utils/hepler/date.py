from datetime import datetime, timedelta


class DateHelper(object):
    @staticmethod
    def split_period(period, step):
        range = list()
        date = datetime.strptime(period[0], '%Y-%m-%d')
        end_date = datetime.strptime(period[1], '%Y-%m-%d')
        while end_date - date >= timedelta(0):
            range.append([date.strftime('%Y-%m-%d'), (date + timedelta(days=step-1)).strftime('%Y-%m-%d')])
            date += timedelta(days=step)
        return range
