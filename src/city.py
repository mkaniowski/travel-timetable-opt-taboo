class City:
    def __init__(self, name, lat, lon, timeSpent, desire):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.timetable = []
        self.timeSpent = timeSpent
        self.desire = desire

    def addTimetable(self, timetable):
        self.timetable = timetable
