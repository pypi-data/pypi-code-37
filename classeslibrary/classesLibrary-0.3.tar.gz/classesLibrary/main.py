from classesLibrary import SubjectContainer


def main():
    SubList = SubjectContainer()
    print(SubList.getReleaseInfo())


    cl = []
    cl=SubList.classes


    print(SubList.getHumanitiesClasses(cl))
    print(SubList.getStrictClasses(cl))




if __name__ == '__main__':
    main()