class Movie(object):

    title = " "
    fantasy = False
    biography = False
    historical = False

    def __init__(self, title, fantasy, biography, historical):
        self.title = title
        self.fantasy = fantasy
        self.biography = biography
        self.historical = historical

    def __str__(self):
        return "Title: " + self.title