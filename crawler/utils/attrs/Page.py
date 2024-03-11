class Page:
    movie = None
    label = None
    director = None
    studio = None
    series = None
    stars = None
    bigimage = None
    categories = None
    sampleimage = None

    def toDict(self):
        return self.__dict__
