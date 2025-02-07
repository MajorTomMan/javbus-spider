class Actress:
    name = ""
    actress_link = ""
    photo_link = ""
    birth_day = ""
    age = ""
    height = ""
    cup = ""
    bust = ""
    waist = ""
    hip = ""
    birth_place = ""
    hobby = ""
    is_censored = ""

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Actress Link: {self.actress_link}\n"
            f"Photo Link: {self.photo_link}\n"
            f"Birth Day: {self.birth_day}\n"
            f"Age: {self.age}\n"
            f"Height: {self.height}\n"
            f"Cup: {self.cup}\n"
            f"Bust: {self.bust}\n"
            f"Waist: {self.waist}\n"
            f"Hip: {self.hip}\n"
            f"Birth Place: {self.birth_place}\n"
            f"Hobby: {self.hobby}"
        )

    def toDict(self):
        return self.__dict__
