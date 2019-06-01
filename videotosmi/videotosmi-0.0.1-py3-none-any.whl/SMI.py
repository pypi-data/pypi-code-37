class SMI:
    def __init__(self, title, lan_name="한국어", lan_code="kr-KR", lan_sort_code="KRCC"):
        self.file_name = title + ".smi"
        self.last_text = ""
        self.lan_code = lan_code
        self.lan_name = lan_name
        self.lan_sort_code = lan_sort_code
        f = open(self.file_name, 'w')
        f.write("<SAMI>\n")
        f.write("<HEAD>\n")
        f.write("<Title>"+ title +"</Title>\n")
        f.write('<STYLE TYPE="text/css">\n')
        f.write("<!--\n")
        f.write("P {margin-left:8pt; margin-right:8pt; margin-bottom:2pt; margin-top:2pt;\n")
        f.write("  text-align:center; font-size:20pt; font-family:arial, sans-serif;\n")
        f.write("  font-weight:normal; color:White;}\n")
        f.write("  ." + self.lan_sort_code + " {Name:" + self.lan_name + "; lang:" + self.lan_code + "; SAMIType:CC;}\n")
        f.write("-->\n")
        f.write("</STYLE>\n")
        f.write("</HEAD>\n\n")
        f.write("<BODY>\n\n")
        f.close()

    def insert(self, text, time, color=None):
        if self.last_text != text:
            start_color = ""
            end_color = ""
            if color is not None:
                start_color = '<font color="' + color + '">'
                end_color = '</font>'
            f = open(self.file_name, 'a')
            f.write("<SYNC Start=" + str(time) + ">\n")
            f.write("<P Class=" + self.lan_sort_code + ">" + start_color + text + end_color + "</P>\n")
            f.write("</SYNC>\n\n")
            f.close()
            self.last_text = text

    def __del__(self):
        f = open(self.file_name, 'a')
        f.write("</BODY>\n")
        f.write("</SAMI>\n")
        f.close()
