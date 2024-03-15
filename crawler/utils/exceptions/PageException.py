class PageException(Exception):
    errorinfo = "Page not Found"

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return self.errorinfo
