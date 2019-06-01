import os
import json
import json5
import argparse
import dconfjson
import subprocess
from glob import glob
from collections import OrderedDict

#dconf reset -f /org/gnome/terminal/legacy/profiles:/
#python setup.py sdist bdist_wheel

parser = argparse.ArgumentParser(description='Import visual studio themes as linux terminal theme profiles')
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

def uuidgen():
    cmd = "(uuidgen)"
    tmp = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE )
    (out, err) = tmp.communicate()
    return out.decode("utf-8").strip()

def dset(dconf_path):
    spath = "/org/gnome/terminal/legacy/profiles:/"
    cmd = ("dconf load %s < %s" % (spath, dconf_path))
    p = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE)
    (out, error) = p.communicate()
    print(out.decode("utf-8"))
    return

def dconf_get():
    spath = "/org/gnome/terminal/legacy/profiles:/"
    cmd = ("dconf dump %s /" % spath)
    p = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE )
    (out, err) = p.communicate()
    return out

def hex2rgb(color):
    tmp = color.lstrip("#")
    if len(tmp) == 3: # for example #AAA
        tmp = "".join([c+c for c in tmp])
        rgb = tuple( int(tmp[i:i+2], 16) for i in (0, 2, 4) )
    elif len(tmp) > 6: # for example #AAAAAA
        rgb = tuple( int(tmp[:6][i:i+2], 16) for i in (0, 2, 4) )
    elif len(tmp) == 6: # for example #AAAAAA
        rgb = tuple( int(tmp[i:i+2], 16) for i in (0, 2, 4) )
    else:
        if args.verbose:
            print("could not convert color: %s to rgb", color)
        return None
    return ("rgb(%d,%d,%d)" % rgb)

def importer():
    # get current dconf
    s_out = dconf_get().decode("utf-8")
    if s_out:
        confjson = dconfjson.dconf_json(s_out)
    else:
        confjson = dconfjson.dconf_json(EMPTY_CONF)

    extensions_folders = []
    # get vscode default themes
    # snap
    extensions_folders.append("/snap/code/current/usr/share/code/resources/app/extensions/")
    # dnf(fedora), 
    extensions_folders.append("/usr/share/code/resources/app/extensions/")
    # get installed vscode theme extensions
    extensions_folders.append("%s/.vscode/extensions/" % os.path.expanduser("~"))
    
    new_profile_added = False
    theme_files = []
    for extensions_folder in extensions_folders:
        for extension in glob("%s*" % extensions_folder):
            extension_name = os.path.basename(extension)
            try:
                with open("%s/package.json" % extension) as fin:
                    a = json.load(fin)
                    for theme in a["contributes"]["themes"]:
                        if "path" in theme:
                            path = extension + theme["path"][1:]
                            uiTheme = "vs-light"
                            if "uiTheme" in theme:
                                uiTheme = theme["uiTheme"]
                            if path.endswith(".json"):
                                theme_files.append([path, uiTheme])
            except:
                None
    for [theme_file, uiTheme] in theme_files:
        # load input data from vscode theme json
        try:
            with open(theme_file) as fin:
                data = json5.load(fin)
        except:
            if args.verbose:
                print("Could not read json config for: %s" % theme_file)
            continue

        if "name" in data:
            name = data["name"]
        else:
            name = " ".join(os.path.basename(theme_file).split("-")[:-1])
            
        if "colors" in data:
            colors = data["colors"]
        else:
            if args.verbose:
                print("%sCould not find colors -- %s%s" % ("\033[91m", "\033[0m", name))
            continue
        
        if uiTheme == "vs-dark":
            mapping = TERMINAL_COLOR_MAP_DARK.copy()
        else:
            mapping = TERMINAL_COLOR_MAP_LIGHT.copy()

        # map data to gnome terminal settings
        for key in mapping:
            if key in data["colors"]:
                if data["colors"][key] != None:
                    mapping[key] = data["colors"][key]
        # set background color
        if "terminal.background" in data["colors"]:
            tmp = data["colors"]["terminal.background"]
        elif uiTheme == "vs-light" and "terminal.ansiWhite" in data["colors"]:
            tmp = data["colors"]["terminal.ansiWhite"]
        elif "editor.background" in data["colors"]:
            tmp = data["colors"]["editor.background"]
        mapping["terminal.background"] = tmp

        # map json colorconfjsonsettings
        palette = []
        for key in mapping:
            if key == "terminal.background":
                break
            palette.append(hex2rgb(mapping[key]))
        background = mapping["terminal.background"]
        foreground = mapping["terminal.foreground"]
        
        # check if theme already exists
        exists = False
        for key in confjson:
            if "visible-name" in confjson[key]:
                if confjson[key]["visible-name"][1:-1] == name:
                    exists = True
                    uuid = key
                    if args.verbose:
                        print("%(y)sProfile exists --%(e)s %(n)s %(y)s-- %(f)s%(e)s" % {"y":"\033[93m", "e":"\033[0m", "n":name, "f":theme_file})
        if not exists:
            # add uuid to list
            uuid = uuidgen()
            confjson[""][" "]["list"] = "%s, '%s']" % (confjson[""][" "]["list"][:-1], uuid)
            # add settings under uuid key
            tmp_confjson= DCONF_DEFAULT.copy()
            tmp_confjson["visible-name"] = "'%s'" % name
            tmp_confjson["palette"] = palette
            tmp_confjson["background-color"] = "'%s'" % hex2rgb(background)
            tmp_confjson["foreground-color"] = "'%s'" % hex2rgb(foreground)             
            confjson[":%s " % uuid] = tmp_confjson
            print("%sInstalled%s  %s" % ("\033[92m", "\033[0m", name))
            new_profile_added = True
    if not new_profile_added:
        print("%sNo new profiles added%s" % ("\033[93m", "\033[0m"))

    #check if first uuid is empty (happens when there were no previous profiles)
    if confjson[""][" "]["list"][1] == ",":
        confjson[""][" "]["list"] = "[" + confjson[""][" "]["list"][2:]
    dconf = dconfjson.json_dconf(confjson)

    # write to file
    with open("output.conf", "w") as fout:
        fout.write(dconf)
    # load into gnome settings
    dset("output.conf")

# Default colors
TERMINAL_COLOR_MAP_LIGHT = OrderedDict([
    ("terminal.ansiBlack", "#000000)"),
    ("terminal.ansiRed", "#cd3131"), 
    ("terminal.ansiGreen", "#00bc00"),
	("terminal.ansiYellow", "#949800"),
	("terminal.ansiBlue", "#0451a5"),
	("terminal.ansiMagenta", "#bc05bc"),
	("terminal.ansiCyan", "#0598bc"),
	("terminal.ansiWhite", "#555555"),
	("terminal.ansiBrightBlack", "#666666"),
	("terminal.ansiBrightRed", "#cd3131"),
	("terminal.ansiBrightGreen", "#14ce14"),
	("terminal.ansiBrightYellow", "#b5ba00"),
	("terminal.ansiBrightBlue", "#0451a5"),
	("terminal.ansiBrightMagenta", "#bc05bc"),
	("terminal.ansiBrightCyan", "#0598bc"),
	("terminal.ansiBrightWhite", "#a5a5a5"),
	("terminal.background", "#ffffff"),
	("terminal.foreground", "#333333")
])

TERMINAL_COLOR_MAP_DARK = OrderedDict([
    ("terminal.ansiBlack", "#000000)"),
    ("terminal.ansiRed", "#cd3131"), 
    ("terminal.ansiGreen", "#0dbc79"),
	("terminal.ansiYellow", "#e5e510"),
	("terminal.ansiBlue", "#2472c8"),
	("terminal.ansiMagenta", "#bc3fbc"),
	("terminal.ansiCyan", "#11a8cd"),
	("terminal.ansiWhite", "#e5e5e5"),
	("terminal.ansiBrightBlack", "#666666"),
	("terminal.ansiBrightRed", "#f14c4c"),
	("terminal.ansiBrightGreen", "#23d18b"),
	("terminal.ansiBrightYellow", "#f5f543"),
	("terminal.ansiBrightBlue", "#3b8eea"),
	("terminal.ansiBrightMagenta", "#d670d6"),
	("terminal.ansiBrightCyan", "#29b8db"),
	("terminal.ansiBrightWhite", "#e5e5e5"),
	("terminal.background", "#1e1e1e"),
	("terminal.foreground", "#cccccc")
])

DCONF_DEFAULT = OrderedDict([
    ("foreground-color", "\'rgb(239,239,227)\'"),
    ("visible-name", None),
    ("palette", None),
    ("cursor-background-color", "\'rgb(0,0,0)\'"),
    ("cursor-colors-set", "false"),
    ("highlight-colors-set", "false"),
    ("use-theme-colors", "false"),
    ("cursor-foreground-color", "\'rgb(255,255,255)\'"),
    ("bold-color-same-as-fg", "true"),
    ("bold-color", "\'rgb(0,0,0)\'"),
    ("background-color", "\'rgb(46,52,54)\'")
])

EMPTY_CONF = "[/]\nlist=[]\ndefault=''"