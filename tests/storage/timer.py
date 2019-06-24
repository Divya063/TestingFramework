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

        return (self.stopTime - self.startTime)

    def val(self):
        return ["%.4f" % float(self.startTime), "%.4f" % float(self.stopTime), self.duration]


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
            return (ms[msl // 2] + ms[msl // 2 + 1]) / 2.0
        else:
            return ms[msl // 2]

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
        return '[measurements: %s, sum: %s, min: %ss, max: %ss, average: %ss, median: %ss]' % (
        len(self.measurements), "%.8f" % float(self.overallSum), "%.8f" % float(self.min), "%.8f" % float(self.max), "%.8f" % float(self.average), "%.8f" % float(self.median))

class Profiling(object):

    def __init__(self):
        self.stats = Measure()
        self.overallStopWatch = StopWatch()
        self.overallStopWatch.start()

    def stop(self):
        self.overallStopWatch.stop()

    def __str__(self):
        return 'Stats: %s' % (self.stats)
