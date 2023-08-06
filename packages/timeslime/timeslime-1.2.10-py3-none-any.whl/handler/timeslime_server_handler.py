from urllib.parse import urljoin
from requests import post

from timeslime.model import Timespan
from timeslime.serializer import TimespanSerializer

class TimeslimeServerHandler():
    def __init__(self, server_url):
        self.server_url = server_url
        self.timespan_route = urljoin(self.server_url, "api/v1/timespans")

    def send_timespan(self, timespan: Timespan) -> Timespan:
        if timespan is None or timespan.start_time is None:
            raise TypeError

        if not self.server_url:
            return timespan

        timespan_serializer = TimespanSerializer()
        data = timespan_serializer.serialize(timespan)
        response = post(self.timespan_route, headers = {'Content-Type': 'application/json'}, data = data)
        response.raise_for_status()
        response_timespan = timespan_serializer.deserialize(response.text)

        return response_timespan