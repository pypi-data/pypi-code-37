


class Subject(object):
    name="none"
    teacher="none"
    humanities= False
    strictClasses= False


    def __init__(self,Name,Teacher,isHumanities,isStrictClasses):
        self.name=Name
        self.teacher=Teacher
        self.isHumanities=isHumanities
        self.isStrictClasses=isStrictClasses

    def __str__(self):


        return "Name: " + self.name + "\nTeacher : " + self.teacher