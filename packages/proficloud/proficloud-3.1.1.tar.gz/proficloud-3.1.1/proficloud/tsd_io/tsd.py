from datetime import datetime, timedelta

import time
from pandas import DataFrame

from streamz.core import Stream
import time
import tornado.ioloop
from tornado import gen

import pandas as pd
import numpy

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from py_linq import Enumerable

##############################

class ProficloudIOMetrics():

    def __init__(self, host='proficloud.io', debug=False):
        self._host = 'tsd.{}'.format(host)
        self._debug = debug

        self._access_token = None
        #self._refresh_token = None

        self.s = requests.Session()
        retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[ 500, 502, 503, 504 ])
        self.s.mount('https://', HTTPAdapter(max_retries=retries))

    def authenticate(self, username, password):
        #Headers:
        auth_header = {
            "Content-Type": "application/json"
        }
        #Payload:
        auth_payload =  {
            "username": username,
            "password": password
        }

        #Send post request
        token_response = requests.post('https://{}/epts/token'.format(self._host), json=auth_payload, headers=auth_header)
        if token_response.ok:
            self._access_token = token_response.json().get("access_token")
            #self._refresh_token = token_response.json().get("refresh_token")
            if self._debug:
                print("Authentication successful!")
            return True
        else:
            print("Authentication error: {}".format(token_response.status_code))

        return False

    def queryMetrics(self, uuid, metrics, start_time=None, end_time=None, dropNa=True, chunkSize=20000, groupIntervalMs=200, aggregator="mean"):
        """
        Query metrics and return the data as pandas DataFrame.
        
        :type metrics: list(str), str
        :param metrics: A list of metric names (or a single metric name) to query. 
        :type start_time: int, datetime, str or None
        :param start_time: Timestamp (ms based), or datetime object (or datetime as string) not used when None. (Default: None)
        :type end_time: int, datetime, str or None
        :param end_time: Timestamp (ms based), or datetime object (or datetime as string). This must be later in time than the start time. If not specified, the end time is assumed to be the current date and time. (Default: None)
        :type dropNa: bool
        :param dropNa: Drop NA when true. Default: True
        :rtype: pandas.DataFrame
        :return: Returns pandas.DataFrame 
        """

        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self._access_token)
        }

        dataFrame = None

        for metric in metrics:
            if self._debug:
                print("Querying metric {}".format(metric), end='', flush=True)

            df = None
            
            while True:
                time.sleep(0.05)

                if self._debug:
                    print('.', end='', flush=True)

                start = start_time
                if df is not None:
                    start = "{}Z".format(df["timestamp"].tail(1).values[0])
                end = end_time

                query = "SELECT {}(value) FROM \"{}\" WHERE (\"uuid\" = '{}') AND time >= '{}' AND time < '{}' GROUP BY time({}ms) fill(none) LIMIT {}".format(aggregator, metric, uuid, start, end, groupIntervalMs, chunkSize)
                if groupIntervalMs == 0:
                    query = "SELECT value FROM \"{}\" WHERE (\"uuid\" = '{}') AND time >= '{}' AND time < '{}' LIMIT {}".format(metric, uuid, start, end, chunkSize)

                url = "https://{}/query?q={}".format(self._host, query)
                result = self.s.get(url, headers=header)
                if not result.ok:
                    print("Error: {};{}".format(result.status_code, result.json()))
                    break

                series = Enumerable(result.json().get("results")).select(lambda s: s.get("series"))
                if series.first_or_default() is None:
                    print("Error: No data for metrics in selected time frame.")
                    break
                data_metric = series.select_many().select(lambda s: s.get("values")).select_many()
                data_df = { "timestamp" : data_metric.select(lambda s: s[0]).to_list(), metric: data_metric.select(lambda s: s[1]).to_list() }
                
                new_df = DataFrame(data_metric, columns=["timestamp", metric])
                new_df["timestamp"] = new_df["timestamp"].map(ProficloudIOMetrics.dateparse)
                
                if df is None:
                    df = new_df 
                else:
                    df = df.append(new_df, ignore_index=True)
                    if len(new_df.index) < chunkSize:
                        break

            if df is not None:            
                df.sort_values("timestamp", inplace=True)
                #Here we have a sorted pandas DF for a single metric + Timestamp

                #Merge with other metrics:
                df.drop_duplicates('timestamp', inplace=True)
                
                if dataFrame is None:
                    dataFrame = df
                else:
                    dataFrame = pd.merge_asof(dataFrame, df, on='timestamp')
                    dataFrame.sort_values("timestamp", inplace=True)

                if self._debug:
                    print('!')
            else:
                print("Unable to query metric {}".format(metric))

        if dropNa:
            dataFrame.dropna(inplace=True)

        #Return final dataframe
        return dataFrame

    @staticmethod
    def dateparse(datestring):
        dateformat = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
        res = datestring
        try:
            res = datetime.strptime(datestring, dateformat[0])
        except:
            res = datetime.strptime(datestring, dateformat[1])
        return res




class MetricsStreamIO(Stream):
    """
    This class creates a "streamz"-stream from a ProvicloudV3Connector (or one of its child classes such as ProficloudMetrics).

    :type connector: ProficloudIOMetrics (or subclass)
    :param connector: An initialized connector.
    :type metrics: list(str), str
    :param metrics: A list of metric names (or a single metric name) to query. 
    :type intervalMs: int
    :param intervalMs: Polling interval in milliseconds
    :type bufferTime: dict
    :param bufferTime: The buffer time is the current date and time minus the specified value and unit. Possible unit values are “milliseconds”, “seconds”, “minutes”, “hours”, “days”, “weeks”, “months”, and “years”. For example, if the start time is 5 minutes, the query will return all matching data points for the last 5 minutes. Example value: { "value": "10", "unit": "minutes" } 
    :type convertTimestamp: boolean
    :param convertTimestamp: Convert the timestamp to datetime (Default: False)
    """

    def __init__(self, connector, uuid, metrics, intervalMs, bufferTime, **kwargs):
        self.__connector = connector
        self.__metrics = metrics
        self.__intervalMs = intervalMs
        self.__bufferTime = bufferTime
        self.__uuid = uuid
        self.header = DataFrame(columns=["timestamp"] + metrics)
        """The header for DataFrame creation with the streamz package"""
        super().__init__(ensure_io_loop=True, **kwargs)
        self.stopped = True

    @gen.coroutine
    def poll_metrics(self):
        """
        Polling co-routine. This retrieves metrics from the connector.
        """
        previousTs = None
        newSamples = None
        lastEmit = None

        while True:

            #Check interval after successful emit:
            if lastEmit is None:
                lastEmit = datetime.utcnow()
            else:
                diffMs = (datetime.utcnow() - lastEmit).total_seconds()*1000
                if diffMs < self.__intervalMs and diffMs > 0:
                    yield(gen.sleep((self.__intervalMs - diffMs)/1000.0))


            try:
                end_t = datetime.utcnow()
                start_t = end_t - self.__bufferTime
                try:
                    currentFrame = self.__connector.queryMetrics(self.__uuid, self.__metrics, start_time=start_t, end_time=end_t, dropNa=True)
                except KeyError as err:
                    #Here, this exception might mean that no data was sent in the requested timedelta. Ignoring
                    currentFrame = None
                    #print(err)
            except:
                raise
                
            if currentFrame is not None:
                if ~currentFrame.empty:
                    if previousTs is not None:
                        newSamples = currentFrame[~currentFrame.timestamp.isin(previousTs)]
                    else:
                        newSamples = currentFrame   
                    previousTs = currentFrame["timestamp"]

                    if (~newSamples.empty) and numpy.array_equal(newSamples.columns, self.header.columns):
                        lastEmit = datetime.utcnow()
                        yield self._emit(newSamples)
                    else:
                        yield gen.sleep(self.__intervalMs/1000.0)
                else:
                    yield gen.sleep(self.__intervalMs/1000.0)
            else:
                yield gen.sleep(self.__intervalMs/1000.0)
            if self.stopped:
                break

    def start(self):
        """
        Start the stream.
        """
        if self.stopped:
            self.stopped = False
            self.loop.add_callback(self.poll_metrics)

    def stop(self):
        """
        Stop the stream.
        """
        if not self.stopped:
            self.stopped = True

    def changeInterval(self, intervalMs):
        self.__intervalMs = intervalMs
