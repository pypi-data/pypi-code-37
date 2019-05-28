import PySimpleGUI as sg
import textwrap
import operator

"""
    A "Live Debugging Tool" - "Watch" your code without stopping it.  Graphical user interface
    Cointains a "REPL" that you can use to run code, etc
"""

PSGDebugLogo = b'R0lGODlhMgAtAPcAAAAAADD/2akK/4yz0pSxyZWyy5u3zZ24zpW30pG52J250J+60aC60KS90aDC3a3E163F2K3F2bPI2bvO3rzP3qvJ4LHN4rnR5P/zuf/zuv/0vP/0vsDS38XZ6cnb6f/xw//zwv/yxf/1w//zyP/1yf/2zP/3z//30wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAyAC0AAAj/AP8JHEiwoMGDCBMqXMiwoUOFAiJGXBigYoAPDxlK3CigwUGLIAOEyIiQI8cCBUOqJFnQpEkGA1XKZPlPgkuXBATK3JmRws2bB3TuXNmQw8+jQoeCbHj0qIGkSgNobNoUqlKIVJs++BfV4oiEWalaHVpyosCwJidw7Sr1YMQFBDn+y4qSbUW3AiDElXiWqoK1bPEKGLixr1jAXQ9GuGn4sN22Bl02roo4Kla+c8OOJbsQM9rNPJlORlr5asbPpTk/RP2YJGu7rjWnDm2RIQLZrSt3zgp6ZmqwmkHAng3ccWDEMe8Kpnw8JEHlkXnPdh6SxHPILaU/dp60LFUP07dfRq5aYntohAO0m+c+nvT6pVMPZ3jv8AJu8xktyNbw+ATJDtKFBx9NlA20gWU0DVQBYwZhsJMICRrkwEYJJGRCSBtEqGGCAQEAOw=='

COLOR_SCHEME = 'LightGreen'

WIDTH_VARIABLES = 12
WIDTH_RESULTS = 36

WIDTH_LOCALS = 80
NUM_AUTO_WATCH = 9

# done purely for testing / show
def func(x=''):
    return 'return value from func()={}'.format(x)


def _non_user_init():
    global watcher_window
    sg.ChangeLookAndFeel(COLOR_SCHEME)
    def InVar(key1, key2):
        row1 = [sg.T('    '),
                sg.I(key=key1, size=(WIDTH_VARIABLES,1)),
                sg.T('',key=key1+'CHANGED_', size=(WIDTH_RESULTS,1)),sg.B('Detail', key=key1+'DETAIL_'),sg.B('Obj', key=key1+'OBJ_'), sg.T(' '),
                sg.T(' '), sg.I(key=key2, size=(WIDTH_VARIABLES, 1)), sg.T('',key=key2 + 'CHANGED_', size=(WIDTH_RESULTS, 1)), sg.B('Detail', key=key2+'DETAIL_'),sg.B('Obj', key=key2+'OBJ_')]
        return row1

    variables_frame = [ InVar('_VAR1_', '_VAR2_'),
                        InVar('_VAR3_', '_VAR4_'),
                        InVar('_VAR5_', '_VAR6_'),]

    interactive_frame = [[sg.T('>>> ', size=(9,1), justification='r'), sg.In(size=(83,1), key='_INTERACTIVE_'), sg.B('Go', bind_return_key=True, visible=False)],
                         [sg.T('CODE >>> ',justification='r', size=(9,1)), sg.In(size=(83, 1), key='_CODE_')],
                         [sg.Multiline(size=(88,12),key='_OUTPUT_',autoscroll=True, do_not_clear=True)],]

    autowatch_frame = [[sg.Button('Choose Variables To Auto Watch', key='_LOCALS_'),
                        sg.Button('Clear All Auto Watches')]] + [
                        [sg.T('', size=(WIDTH_VARIABLES,1), key='_WATCH%s_'%i),
                         sg.T('', size=(WIDTH_RESULTS,2), key='_WATCH%s_RESULT_'%i)] for i in range(1,NUM_AUTO_WATCH+1)]

    layout = [  [sg.Frame('Variables or Expressions to Watch', variables_frame, title_color='blue' )],
                [sg.Frame('REPL-Light - Press Enter To Execute Commands', interactive_frame, title_color='blue' ),sg.Frame('Auto Watches', autowatch_frame, title_color='blue' )],
                [sg.Button('Ok')]]

    window = sg.Window("I'm Watching You Debugger", layout, icon=PSGDebugLogo).Finalize()
    window.Element('_VAR1_').SetFocus()
    watcher_window = window
    sg.ChangeLookAndFeel('SystemDefault')
    return window

def _event_once(mylocals, myglobals):
    global myrc, watcher_window, local_choices
    if not watcher_window:
        return False
    # _window = watcher_window
    event, values = watcher_window.Read(timeout=1)
    if event in (None, 'Exit Debugger'):                             # EXIT BUTTON / X BUTTON
        watcher_window.Close()
        watcher_window = None
        return False

    cmd_interactive = values['_INTERACTIVE_']
    cmd_code = values['_CODE_']
    cmd = cmd_interactive or cmd_code

    if event == 'Go':                                       # GO BUTTON
        watcher_window.Element('_INTERACTIVE_').Update('')
        watcher_window.Element('_CODE_').Update('')
        watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)
        if cmd_interactive:
            expression = """
global myrc
imwatchingyou.imwatchingyou.myrc = {} """.format(cmd)
            try:
                exec(expression, myglobals, mylocals)
                watcher_window.Element('_OUTPUT_').Update('{}\n'.format(myrc),append=True, autoscroll=True)

            except Exception as e:
                watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e),append=True, autoscroll=True)
        else:
            watcher_window.Element('_CODE_').Update('')
            watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)
            expression = """
{}""".format(cmd)
            try:
                exec(expression, myglobals, mylocals)
                watcher_window.Element('_OUTPUT_').Update('{}\n'.format(cmd), append=True, autoscroll=True)

            except Exception as e:
                watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e), append=True, autoscroll=True)

    elif event.endswith('_DETAIL_'):                        # DETAIL BUTTON
        var = values['_VAR{}_'.format(event[4])]
        expression = """
global myrc
imwatchingyou.imwatchingyou.myrc = {} """.format(var)
        try:
            exec(expression, myglobals, mylocals)
            sg.PopupScrolled(str(values['_VAR{}_'.format(event[4])]) + '\n' + str(myrc), title=var, non_blocking=True)
        except:
            print('Detail failed')
    elif event.endswith('_OBJ_'):                            # OBJECT BUTTON
        var = values['_VAR{}_'.format(event[4])]
        expression = """
global myrc
imwatchingyou.imwatchingyou.myrc = {} """.format(var)
        try:
            exec(expression, myglobals, mylocals)
            sg.PopupScrolled(sg.ObjToStringSingleObj(myrc),title=var, non_blocking=True)
        except:
            print('Detail failed')
    elif event == '_LOCALS_':     # Show all locals BUTTON
        _choose_auto_watches(mylocals)
    elif event == 'Clear All Auto Watches':
        if sg.PopupYesNo('Do you really want to clear all Auto-Watches?', 'Really Clear??') == 'Yes':
            local_choices = {}
    # -------------------- Process the manual "watch list" ------------------
    for i in range(1, 7):
        key = '_VAR{}_'.format(i)
        out_key = '_VAR{}_CHANGED_'.format(i)
        myrc =''
        if watcher_window.Element(key):
            if values[key]:
                expression = """
global myrc
imwatchingyou.imwatchingyou.myrc = {} """.format(values[key])
                try:
                    exec(expression, myglobals, mylocals)
                except Exception as e:
                    pass
                watcher_window.Element(out_key).Update(myrc)
            else:
                watcher_window.Element(out_key).Update('')

    # -------------------- Process the automatic "watch list" ------------------
    slot = 1
    for key in local_choices:
        if local_choices[key]:
            watcher_window.Element('_WATCH{}_'.format(slot)).Update(key)
            expression = """
global myrc
imwatchingyou.imwatchingyou.myrc = {} """.format(key)
            try:
                exec(expression, myglobals, mylocals)
                watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(myrc)
            except Exception as e:
                watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update('')
            slot += 1
            if slot >= NUM_AUTO_WATCH:
                break
    for i in range(slot, NUM_AUTO_WATCH+1):
        watcher_window.Element('_WATCH{}_'.format(i)).Update('')
        watcher_window.Element('_WATCH{}_RESULT_'.format(i)).Update('')

    return True


def _choose_auto_watches(my_locals):
    global local_choices
    sg.ChangeLookAndFeel(COLOR_SCHEME)
    num_cols = 3
    output_text = ''
    num_lines = 2
    cur_col = 0
    layout = [[sg.Text('Choose your "Auto Watch" variables', font='ANY 14', text_color='red')]]
    longest_line = max([len(key) for key in my_locals])
    line = []
    sorted_dict = {}
    for key in sorted(my_locals.keys()):
        sorted_dict[key] = my_locals[key]
    for key in sorted_dict:
        line.append(sg.CB(key, key=key, size=(longest_line,1), default=local_choices[key] if key in local_choices else False))
        if cur_col +1 == num_cols:
            cur_col = 0
            layout.append(line)
            line = []
        else:
            cur_col += 1
    layout += [[sg.Ok(), sg.Cancel(), sg.Btn('Clear All')]]

    window = sg.Window('All Locals', layout, icon=PSGDebugLogo).Finalize()

    while True:             # event loop
        event, values = window.Read()
        if event in (None, 'Cancel'):
            break
        elif event == 'Ok':
            local_choices = values
            break
        elif event == 'Clear All':
            for key in sorted_dict:
                window.Element(key).Update(False)
                sg.PopupQuickMessage('Cleared Auto Watches', auto_close=True, auto_close_duration=3, non_blocking=True, text_color='red', font='ANY 18')
    # exited event loop
    window.Close()
    sg.ChangeLookAndFeel('SystemDefault')

def refresh(locals, globals):
    return _event_once(locals, globals)

def initialize():
    global watcher_window
    watcher_window = _non_user_init()

myrc = ''
watcher_window = None
local_choices = {}


if __name__ == '__main__':
    initialize()
    while True:
        refresh(locals(), globals())