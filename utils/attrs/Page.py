class Page:
    movie=None
    label=None
    director = None
    studio = None
    series = None
    stars=None
    images=None
    categories=None
    def __str__(self):
        properties = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return "\n".join(properties)
    def toDict(self):
        return self.__dict__