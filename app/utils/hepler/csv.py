import csv


class CsvReader(object):
    @staticmethod
    def get_reader(path, delimiter=','):
        file_handler = open(path, 'r')
        return csv.DictReader(file_handler, delimiter=delimiter)


class CsvWriter(object):
    @staticmethod
    def write_data(path, data, delimiter=','):
        with open(path, 'w') as file_handler:
            writer = csv.writer(file_handler, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)
