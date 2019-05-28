#!/usr/bin/env python
import argparse
import gitbuilding as gb
import os
import codecs


def main():
    parser = argparse.ArgumentParser(description='Run git building to build your documentation')
    #TODO add subparsers for the functions
    parser.add_argument('command',help="Posible options: 'build', 'new', and 'serve'")
    args = parser.parse_args()
    
    if args.command == 'build':
        if os.path.isfile('buildconf.yaml'):
            doc = gb.Documentation('buildconf.yaml')
            doc.buildall()
        else:
            print("\n\nCannot build here. Not a valid gitbuilding directory: No 'buildconf.yaml' found\n")
            return None
    elif args.command == 'new':
        if os.listdir('.') == []:
            newdir = '.'
        else:
            ans =  input('This directory is not empty. Build to new sub-dir? [y/N]: ')
            if ans == 'y' or ans == 'Y':
                newdir = input('Enter subdir name: ')
                if not os.path.split(newdir)[0]=='':
                    print('\n\ngitbuilding new only supports creating a single subdirectory to the current folder, not nested directories or full paths\n\n')
                    return None
                if os.path.exists(newdir):
                    print(f"\n\nCannot create directory '{newdir}', as it already exists\n\n")
                    return None
                try:
                    os.mkdir(newdir)
                except:
                    print(f"\n\nFailed to create directory '{newdir}'\n\n")
                    return None
            else:
                if not (ans == 'n' or ans == 'N' or ans == ''):
                    print('Invalid response.')
                return None
        # writing default/empty project
        
        #CONFIG FILE
        with codecs.open(os.path.join(newdir,'buildconf.yaml'), "w", "utf-8") as file:
            file.write(gb.empty.emptyconfig())
        
        #OVERVIEW FILE
        with codecs.open(os.path.join(newdir,'overview.md'), "w", "utf-8") as file:
            file.write(gb.empty.emptyoverview())
        
        #TESTPAGES
        for page in ['testpage1.md','testpage2.md']:
            with codecs.open(os.path.join(newdir,page), "w", "utf-8") as file:
                file.write(gb.empty.testpage(page))
        
        #PARTS LIST
        with codecs.open(os.path.join(newdir,'Parts.yaml'), "w", "utf-8") as file:
            file.write(gb.empty.basicparts())
        
    elif args.command == 'serve':
        doc = gb.Documentation('buildconf.yaml')
        gbs = gb.GBServer(os.path.join('Output',doc.overview))
        gbs.run()
    else:
        print(f'Invalid gitbuilding command {args.command}')
        return None

if __name__ == '__main__':
    main() 
