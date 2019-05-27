import os
import time

class StopWatch(object):

    def __init__(self):
        self.startTime = None
        self.stopTime = None

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.stopTime = time.time()

    @property
    def duration(self):
        if((self.startTime == None) or (self.stopTime == None)):
            return None

        return self.stopTime - self.startTime

    def __str__(self):
        return '%ss ' % self.duration


class Measure(object):
    def __init__(self):
        self.measurements = []

    def startMeasurement(self):
        timing = StopWatch()

        self.measurements.append(timing)

        timing.start()

        return timing

    @property
    def min(self):
        minTime = None

        for time in self.measurements:
            currTime = time.duration

            if (currTime == None):
                continue

            if ((minTime == None) or (currTime < minTime)):
                minTime = currTime

        return minTime

    @property
    def max(self):
        maxTime = None

        for time in self.measurements:
            currTime = time.duration

            if (currTime == None):
                continue

            if ((maxTime == None) or (currTime > maxTime)):
                maxTime = currTime

        return maxTime

    @property
    def average(self):
        measLen = len(self.measurements)

        if (measLen == 0):
            return None

        os = self.overallSum
        if (os == None):
            return None

        # TODO divide through the number of not None durations
        return os / measLen

    @property
    def median(self):
        ms = [m.duration for m in self.measurements if m.duration != None]

        ms.sort()

        msl = len(ms)
        if (msl == 0):
            return None

        if (msl % 2 == 0):
            return (ms[msl / 2] + ms[msl / 2 + 1]) / 2.0
        else:
            return ms[msl / 2]

    @property
    def overallSum(self):
        sum = 0.0

        for m in self.measurements:
            d = m.duration
            if (d == None):
                continue

            sum += d

        return sum

    def __str__(self):
        # TODO add median
        return '[measurements: %s, sum: %s, min: %ss, max: %ss, average: %ss, median: %ss]' % (
        len(self.measurements), self.overallSum, self.min, self.max, self.average, self.median)

class Profiling(object):

    def __init__(self):
        self.stats = Measure()

        self.overallStopWatch = StopWatch()

    def start(self):
        self.overallStopWatch.start()

    def stop(self):
        self.overallStopWatch.stop()
        self.stats.startMeasurement()

    def __str__(self):
        return 'Stats: %s\nOverall time: %s\n' % (self.stats, self.overallStopWatch)