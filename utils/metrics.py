import time
from collections import defaultdict

class Metrics:
    def __init__(self):
        self.data = defaultdict(int)
        self.timings = defaultdict(list)

    
        self.active_videos = set()   
        self.start_times = {}        


    def inc(self, key, value=1):
        self.data[key] += value


    def time_start(self):
        return time.time()

    def time_end(self, key, start):
        self.timings[key].append(time.time() - start)

    def get_avg(self, key):
        if not self.timings[key]:
            return 0
        return sum(self.timings[key]) / len(self.timings[key])


    def snapshot(self):
        return {
            "counters": dict(self.data),
            "timings_avg": {
                k: self.get_avg(k) for k in self.timings
            }
        }

    def is_new_video(self, video_id: str) -> bool:
        """
        Prevent duplicate processing (for caching layer later)
        """
        if video_id in self.active_videos:
            return False
        self.active_videos.add(video_id)
        return True

    def reset_video(self, video_id: str):
        """
        Optional cleanup hook (future scaling / cache expiry)
        """
        self.active_videos.discard(video_id)


metrics = Metrics()