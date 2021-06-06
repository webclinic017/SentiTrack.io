import datetime
class DateTimeRangeMap:

    """
    A data structure to store and lookup values by datetime key
    Stores a tuple of datetime range as a key and list as value
    Keeps a sorted array of intervals
    """

    def __init__(self, now, interval, historical = False):
        #initialize the intervals
        min = datetime.timedelta(minutes = interval)
        if historical:
            it = datetime.timedelta(minutes = interval - 1)
            end_range = [now - (min * i) for i in range(0, 60//interval)][::-1]
            last = now - it
            start_range = [last- (min * i) for i in range(0, 60//interval)][::-1]
            self.range_map = [(x,y) for x,y in zip(start_range, end_range)]
        else:
            start = now - min
            self.range_map = [[(start, now), []]]
    
    def insert(self, key, value):

        """
        Runs binary search to place value into correct range for the given key
        """

        start = 0
        end = len(self.range_map) - 1
        while start <= end:
            mid = (start + end) // 2
            range = self.range_map[mid][0]
            if range[0] <= key <= range[1]:
                self.range_map[mid][1].append(value)
                return 1
            elif key < range[0]:
                end = mid - 1
            else:
                start = mid + 1
        return -1

