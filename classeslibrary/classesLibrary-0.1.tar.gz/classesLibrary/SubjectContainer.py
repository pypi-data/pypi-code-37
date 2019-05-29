from classesLibrary.Subject import Subject

class   SubjectContainer(object):
    classes = []

    def __init__(self):
        self.classes.append(Subject("Math", "John Smith", False, True))
        self.classes.append(Subject("Physics", "Nate Kovalsky", False, True))
        self.classes.append(Subject("Biology", "Anna Bell", False, True))

        self.classes.append(Subject("Polish language", "Małgorzata Pelczar", True, False))
        self.classes.append(Subject("History", "Marek Kołcon", True, False))
        self.classes.append(Subject("Knowledge of culture", "J.A Graham", True, False))


    def getStrictClasses(self, classes):

        for i in classes:
            if self.classes[i].isStrictClasses == True:
                print(classes[i])

    def getHumanitiesClasses(self,classes):

        for i in classes:
            if self.classes[i].humanities == True:
                print(classes[i])

