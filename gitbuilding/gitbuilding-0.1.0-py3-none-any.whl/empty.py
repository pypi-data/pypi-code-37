

def emptyconfig():
    return '''OverviewPage: overview.md

#uncomment below to add custom categories
#CustomCategories:
#    PrintedTool:
#        Reuse: False

#uncomment below to set custom category
# DefaultCategory: PrintedTool

#List of YAML part libraries
PartLibs:
    - Parts

#uncomment below to disable fussy warnings
#Fussy: False'''

def emptyoverview():
    return '''# Test Project

This is a great place to start making your documentation!

You should link to a couple of pages:

* [.](testpage1.md)
* [.](testpage2.md)

And you should definitly let people know about the {{BOMlink}} page.'''

def testpage(Name):
    return '''[M4x10 screws]:Parts/M4x10PanSteel.md "Qty: 5"
# %s


{{BOM}}

## Method
This page should have some instructions for things in your project instead it just has a link for three [M4x10 screws]{Qty: 3} and another link to use [two more][M4x10 screws]{Qty: 2}.'''%Name

def basicparts():
    return '''
M4x10PanSteel:
    Name: M4x10 Pan Head Steel
    Description: >
        This is lots of text
        about some screw?
    Specs:
        Head: Pan
        Length: 10 mm
        Material: Stainless Steel
        Pitch: 0.7
    Suppliers:
        RS:
            PartNo: 528-817
            Link: https://uk.rs-online.com/web/p/machine-screws/0528817/
        McMasterCarr:
            PartNo: 90116A207
            Link: https://www.mcmaster.com/90116A207'''