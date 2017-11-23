from apiclient.discovery import build
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials


class GoogleAnalytic(object):
    _ga = None
    _view_id = None

    def __init__(self, **kwargs):
        self._view_id = kwargs['view_id']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            kwargs['key_file_location'],
            kwargs['scopes']
        )

        # Build the service object.
        self._ga = build('analytics', 'v4', credentials=credentials)

    def _get_response(self, conditions):
        body = {
            'reportRequests': [
                {
                    'pageSize': conditions.get('pageSize'),
                    'viewId': self._view_id,
                    'dateRanges': conditions.get('dateRanges'),
                    'metrics': conditions.get('metrics', []),
                    'dimensions': conditions.get('dimensions', []),
                    'dimensionFilterClauses': conditions.get('dimensionsFilterClauses', [])
                }]
        }

        return self._ga.reports().batchGet(body=body).execute()

    def get_data(self, params):

        conditions = dict(
            pageSize=30000,
            dateRanges=[dict(startDate=params.get('from_'), endDate=params.get('to_'))]
        )
        if 'metrics' in params:
            conditions['metrics'] = [dict(expression=metric) for metric in params.get('metrics')]
        if 'dimensions' in params:
            conditions['dimensions'] = [dict(name=dimension) for dimension in params.get('dimensions')]
        if 'dimensions_filter' in params:
            conditions['dimensionsFilterClauses'] = self._build_dimensions_filter(params.get('dimensions_filter'))

        response = self._get_response(conditions)
        return self._pretty(response)

    @staticmethod
    def _build_dimensions_filter(dimensions_filters):
        return [
            dict(
                operator=dimensions_filters.get('operator') if 'operator' in dimensions_filters else "OR",
                filters=[f for f in dimensions_filters.get('filters')]
            )
        ]

    @staticmethod
    def _pretty(response):
        reporter = []
        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                dateRangeValues = row.get('metrics', [])
                metrics = dateRangeValues[0].get('values')
                d = dict((dimensionHeaders[i], dimensions[i]) for i in range(0, len(dimensionHeaders)))
                m = dict((metricHeaders[i]['name'], int(metrics[i])) for i in range(0, len(metricHeaders)))
                reporter.append({**d, **m})

        return reporter
