class Movie:
    title=""
    code=""
    link=""
    release_date=""
    length=""
    def toDict(self):
        return self.__dict__