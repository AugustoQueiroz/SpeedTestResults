from __future__ import annotations

from dateutil.parser import parse
import datetime
import json

class SpeedTestLoggerResults:
    @staticmethod
    def load(results_file_path: str) -> SpeedTestLoggerResults:
        results = []
        with open(results_file_path) as results_file:
            for line in results_file:
                results.append(json.loads(line))
        
        return SpeedTestLoggerResults(results)
    
    def __init__(self, result_jsons: [dict]):
        self.results = result_jsons

        for result in self.results:
            result['timestamp'] = self.__parse_timestamp(result['timestamp'])

    def __parse_timestamp(self, ts: str) -> datetime.datetime:
        return parse(ts).replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

    def plot_hist(self, keys, bins=10, map_fn=None):
        import matplotlib.pyplot as plt

        filtered_results = self[keys]
        if map_fn is not None:
            filtered_results = list(map(map_fn, filtered_results))

        ax = plt.subplot(111)
        ax.hist(filtered_results, bins=bins)
        return ax
    
    def __getitem__(self, keys):
        filtered = self.results
        if isinstance(keys, str):
            keys = (keys, )
        if isinstance(keys, tuple):
            for key in keys:
                filtered = [f[key] for f in filtered]
        return filtered