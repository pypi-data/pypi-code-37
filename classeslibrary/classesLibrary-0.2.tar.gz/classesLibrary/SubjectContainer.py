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


    def getStrictClasses(self,classes):
        classesLenght = len(classes)
        temp=[]
        for i in range(classesLenght):
            if self.classes[i].strictClasses is True:
                 temp.append(classes[i])
        for i in range(3):
            print(temp[i])

    def getHumanitiesClasses(self,classes):
        classesLenght = len(classes)
        temp=[]
        for i in range(classesLenght):
            if self.classes[i].humanities is True:
                temp.append(classes[i])
        for i in range(3):
            print(temp[i])

    def getReleaseInfo(self):
        return "Release version v0.1"

