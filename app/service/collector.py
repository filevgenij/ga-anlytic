from datetime import datetime


class Collector(object):
    _ga = None
    _session_service = None
    _scene_service = None
    _band_service = None
    _download_service = None
    _referrer_service = None
    _language_service = None

    def __init__(self,
                 ga,
                 session_service,
                 scene_service,
                 band_service,
                 download_service,
                 referrer_service,
                 language_service):
        self._ga = ga
        self._session_service = session_service
        self._scene_service = scene_service
        self._band_service = band_service
        self._download_service = download_service
        self._referrer_service = referrer_service
        self._language_service = language_service
        super().__init__()

    def collect_session(self, period, progress_bar):
            session_data = self._ga.get_data(dict(
                from_=period[0],
                to_=period[1],
                metrics=['ga:sessions'],
                dimensions=['ga:date', 'ga:dimension1']
            ))
            progress_bar.set_redraw_frequency(500)
            progress_bar.start(len(session_data))
            for row in session_data:
                if row['ga:dimension1'].isnumeric():
                    self._session_service.insert([
                        int(row['ga:dimension1']),
                        datetime.strptime(row['ga:date'], '%Y%M%d').strftime('%Y-%M-%d'),
                        int(row['ga:sessions'])
                    ])
                progress_bar.advance()
            progress_bar.finish()

    def collect_scene(self, period, progress_bar):
        band_data = self._ga.get_data(dict(
            from_=period[0],
            to_=period[1],
            metrics=['ga:sessions', 'ga:uniqueEvents', 'ga:totalEvents'],
            dimensions=['ga:eventCategory', 'ga:eventAction', 'ga:eventLabel', 'ga:date', 'ga:dimension1'],
            dimensions_filter=dict(
                filters=[dict(
                    dimensionName='ga:eventCategory',
                    operator='EXACT',
                    expressions=['Scenes']
                )]
            )
        ))
        progress_bar.set_redraw_frequency(500)
        progress_bar.start(len(band_data))
        for row in band_data:
            if row['ga:dimension1'].isnumeric():
                self._scene_service.insert([
                    int(row['ga:dimension1']),
                    datetime.strptime(row['ga:date'], '%Y%M%d').strftime('%Y-%M-%d'),
                    row['ga:eventAction'],
                    row['ga:eventLabel'],
                    row['ga:uniqueEvents'],
                    row['ga:totalEvents']
                ])
            progress_bar.advance()
        progress_bar.finish()

    def collect_band(self, period, progress_bar):
        band_data = self._ga.get_data(dict(
            from_=period[0],
            to_=period[1],
            metrics=['ga:sessions', 'ga:uniqueEvents', 'ga:totalEvents'],
            dimensions=['ga:eventCategory', 'ga:eventAction', 'ga:eventLabel', 'ga:date', 'ga:dimension1'],
            dimensions_filter=dict(
                filters=[dict(
                    dimensionName='ga:eventCategory',
                    operator='EXACT',
                    expressions=['Bands']
                )]
            )
        ))
        progress_bar.set_redraw_frequency(500)
        progress_bar.start(len(band_data))
        for row in band_data:
            if row['ga:dimension1'].isnumeric():
                self._band_service.insert([
                    int(row['ga:dimension1']),
                    datetime.strptime(row['ga:date'], '%Y%M%d').strftime('%Y-%M-%d'),
                    row['ga:eventLabel'],
                    row['ga:uniqueEvents'],
                    row['ga:totalEvents']
                ])
            progress_bar.advance()
        progress_bar.finish()

    def collect_download(self, period, progress_bar):
        download_data = self._ga.get_data(dict(
            from_=period[0],
            to_=period[1],
            metrics=['ga:sessions', 'ga:uniqueEvents', 'ga:totalEvents'],
            dimensions=['ga:eventCategory', 'ga:eventAction', 'ga:eventLabel', 'ga:date', 'ga:dimension1'],
            dimensions_filter=dict(
                filters=[dict(
                    dimensionName='ga:eventCategory',
                    operator='EXACT',
                    expressions=['Downloads']
                )]
            )
        ))
        progress_bar.set_redraw_frequency(500)
        progress_bar.start(len(download_data))
        for row in download_data:
            if row['ga:dimension1'].isnumeric():
                self._download_service.insert([
                    int(row['ga:dimension1']),
                    datetime.strptime(row['ga:date'], '%Y%M%d').strftime('%Y-%M-%d'),
                    row['ga:eventAction'],
                    row['ga:eventLabel'],
                    row['ga:uniqueEvents'],
                    row['ga:totalEvents']
                ])
            progress_bar.advance()
        progress_bar.finish()

    def collect_referrer(self, period, progress_bar):
        user_ids = set()
        referrer_data = self._ga.get_data(dict(
            from_=period[0],
            to_=period[1],
            metrics=['ga:sessions'],
            dimensions=['ga:dimension1', 'ga:date', 'ga:fullReferrer']
        ))
        progress_bar.set_redraw_frequency(500)
        progress_bar.start(len(referrer_data))
        for row in referrer_data:
            if row['ga:dimension1'].isnumeric():
                user_ids.add(int(row['ga:dimension1']))
                self._referrer_service.insert([
                    int(row['ga:dimension1']),
                    datetime.strptime(row['ga:date'], '%Y%M%d').strftime('%Y-%M-%d'),
                    row['ga:fullReferrer']
                ])
            progress_bar.advance()
        progress_bar.finish()
        return user_ids

    def collect_language(self, period, progress_bar):
        language_data = self._ga.get_data(dict(
            from_=period[0],
            to_=period[1],
            metrics=['ga:sessions'],
            dimensions=['ga:language', 'ga:dimension1']
        ))
        progress_bar.set_redraw_frequency(500)
        progress_bar.start(len(language_data))
        for row in language_data:
            if row['ga:dimension1'].isnumeric() and row['ga:language'] != '(not set)':
                self._language_service.insert([
                    int(row['ga:dimension1']),
                    row['ga:language']
                ])
            progress_bar.advance()
        progress_bar.finish()
