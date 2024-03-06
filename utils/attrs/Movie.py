class Movie:
    title=""
    code=""
    release_date=""
    length=""
    big_image_link=""
    sample_image_links=[]
    stars={}
    director = None
    studio = None
    categorys = []
    genres = None
    series = None
    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"Code: {self.code}\n"
            f"Release Date: {self.release_date}\n"
            f"Length: {self.length}\n"
            f"Big Image Link: {self.big_image_link}\n"
            f"Sample Image Links: {', '.join(self.sample_image_links)}\n"
            f"Stars: {', '.join(self.stars.keys())}\n"
            f"Director: {self.director}\n"
            f"Studio: {self.studio}\n"
            f"Categorys: {', '.join(self.categorys)}\n"
            f"Genres: {self.genres}\n"
            f"Series: {self.series}"
        )