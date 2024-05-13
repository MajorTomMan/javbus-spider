class Page:
    movie = None
    label = None
    director = None
    studio = None
    series = None
    actresses = None
    bigimage = None
    categories = None
    sampleimage = None
    magnets = None

    def toDict(self):
        return self.__dict__
