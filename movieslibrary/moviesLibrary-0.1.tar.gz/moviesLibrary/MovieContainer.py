from moviesLibrary.Movie import Movie


class MovieContainer(object):
    movies = []

    def __init__(self):
        self.movies.append(Subject("Title1", True, False, False))
        self.movies.append(Subject("Title2", False, True, False))
        self.movies.append(Subject("Title3", False, False, True))
        self.movies.append(Subject("Title4", True, False, False))
        self.movies.append(Subject("Title5", False, True, False))
        self.movies.append(Subject("Title6", False, False, True))

    def getHistorical(self, movies):
        movie_len = len(movies)
        tmp = []
        for i in range(movie_len):
            if self.movies[i].historical is True:
                tmp.append(movies[i])
        tmp_len = len(tmp)
        for i in range(tmp_len):
            print(tmp[i])

    def getFantasy(self, movies):
        movie_len = len(movies)
        tmp = []
        for i in range(movie_len):
            if self.movies[i].fantasy is True:
                tmp.append(movies[i])

    def getBiography(self, movies):
        movie_len = len(movies)
        tmp = []
        for i in range(movie_len):
            if self.movies[i].biography is True:
                tmp.append(movies[i])


    def getReleaseInfo(self):
        return "v0.1"
