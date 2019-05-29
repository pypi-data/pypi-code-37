


class Subject(object):
    name=""
    teacher=""
    humanities= False
    strictClasses= False


    def __init__(self,Name,Teacher,isHumanities,isStrictClasses):
        self.name=Name
        self.teacher=Teacher
        self.humanities=isHumanities
        self.strictClasses=isStrictClasses

    def __str__(self):
        return "\nName: " + self.name + "\nTeacher : " + self.teacher +"\n "