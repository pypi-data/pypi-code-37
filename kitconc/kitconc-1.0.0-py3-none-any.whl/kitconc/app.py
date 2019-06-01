# -*- coding: utf-8 -*-
import os, sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox 
from  tkinter import simpledialog
from multiprocessing import Process
import kitconc
from kitconc.corpus import Corpus 
import time 
import pickle 
import shutil

class frmNewCorpus(Toplevel):
    def __init__(self,master=None,**kwargs):
        self.master = master
        self.root = Toplevel(master)
        self.root.resizable(False, False)
        self.root.title('New corpus...')
        window_height = 170
        window_width = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.__load()
        
    def __load(self):
        self.lbl_Name = ttk.Label(self.root,text='Name:')
        self.lbl_Name.place(x=10,y=10)
        self.txt_Name = ttk.Entry(self.root)
        self.txt_Name.place(x=15,y=30)
        self.lbl_Language = ttk.Label(self.root,text='Language:')
        self.lbl_Language.place(x=10,y=50)
        self.cmb_Language = ttk.Combobox(self.root,state='readonly',width=10, values=['portuguese','english'])
        self.cmb_Language.place(x=10,y=70)
        self.cmb_Language.current(1)
        self.lbl_Encoding = ttk.Label(self.root,text='Encoding:')
        self.lbl_Encoding.place(x=10,y=90)
        self.cmb_Encoding = ttk.Combobox(self.root,state='readonly',width=10, values=['latin-1','utf-8'])
        self.cmb_Encoding.place(x=10,y=110)
        self.cmb_Encoding.current(1)
        self.btn_Save = ttk.Button(self.root,text='Save',width=6,command=self.__command_Save)
        self.btn_Save.place(x=10,y=140)
        self.btn_Cancel = ttk.Button(self.root,text='Cancel',width=6,command=self.__command_Cancel)
        self.btn_Cancel.place(x=70,y=140)
        self.txt_Name.focus()
    
    def __command_Save(self,event=None):
        workspace = self.master.config['workspace'] 
        name = self.txt_Name.get() 
        name = name.strip().replace(' ','_')
        language = self.cmb_Language.get()
        encoding = self.cmb_Encoding.get()
        if len(name)==0:
            messagebox.showwarning('Attention!', message='Name is invalid.')
            self.__command_Cancel()
        else:
            self.process = Process(target=lambda:self.__process_Start(workspace,name,language,encoding))  
            self.process.daemon = True
            self.process.start()
            self.root.after(20, self.__process_Check) 

    def __process_Start(self,workspace,name,language,encoding):
        corpus = Corpus(workspace,name,language=language,encoding=encoding)
        
    def __process_Check(self,event=None):
        if self.process.is_alive():
            self.root.after(20, self.__process_Check)
        else:
            self.master.update_corpora()
            messagebox.showinfo('Success!',message='Your corpus in available now.')
            self.__command_Cancel()

    def __command_Cancel(self, event=None):
        try:
            self.root.destroy()
        except:
            pass 
     

class frmWordlist (Toplevel):
    def __init__(self,master=None,**kwargs):
        self.master = master
        self.root = Toplevel(master)
        self.root.width = 300
        self.root.height = 200
        self.root.resizable(False, False)
        self.root.title('Wordlist')
        window_height = 200
        window_width = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.__load()
        self.focus_force()
        

    
    def __load(self):
        self.btn_Run = ttk.Button(self.root,text='Run',width=6,command=self.__start_submit_process)
        self.btn_Run.place(x=10,y=170)
        self.btn_Stop = ttk.Button(self.root,text='Stop',width=6,command=self.__stop_submit_process)
        self.btn_Stop.place(x=70,y=170)
        self.btn_Cancel = ttk.Button(self.root,text='Cancel',width=6,command=self.__action_cancel)
        self.btn_Cancel.place(x=130,y=170)
        self.pgb_Progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.pgb_Progress.place(x=190,y=172)

    
    def __start_submit_process(self,event=None):
        self.submit_process = Process (target=self.__action_submit_process)
        self.submit_process.daemon = True
        self.pgb_Progress['mode'] = 'indeterminate'
        self.pgb_Progress.start()
        self.submit_process.start()
        self.root.after(20, self.__check_submit_process) 
    
    def __stop_submit_process(self,event=None):
        self.submit_process.terminate()
        
    
    def __check_submit_process(self,event=None):
        if self.submit_process.is_alive():
            self.root.after(20, self.__check_submit_process)
        else:
            self.pgb_Progress.stop()
            self.pgb_Progress['mode'] = 'determinate'
            self.root.destroy()

    def __action_submit_process(self,event=None):
        workspace = self.master.config['workspace']
        corpus_name = self.master.config['corpus']
        corpus = Corpus(workspace,corpus_name)
        wordlist = corpus.wordlist(show_progress=True)
        wordlist.save_excel(corpus.output_path + '/wordlist.xlsx')
        
         


    def __action_wordlist(self,event=None):
        try:
            self.submit_process.terminate()
        except:
            pass 
    
    def __action_cancel(self,event=None):
        try:
            self.submit_process.terminate()
        except:
            pass 
        self.root.destroy()



        

class KitconcApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.title('Kitconc ' + kitconc.__version__)
        self.resizable(False, False)  
        window_height = 600
        window_width = 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.running = True
        self.__load()


    def __load(self):
        # load config
        self.__check_config_file()
        # corpus
        self.lbl_Corpus = Label(self,text='Corpus')
        self.lbl_Corpus.place(x=10,y=10)
        self.cmb_Corpus  = ttk.Combobox(self,state='readonly',width=20)
        self.cmb_Corpus.place(x=10,y=30) 
        self.cmb_Corpus.bind("<<ComboboxSelected>>", self.__action_select_corpus)
        self.btn_Corpus = ttk.Button(text='New...',width=6,command=self.__new_corpus)
        self.btn_Corpus.place(x=10,y=50)
        
        self.btn_AddTexts = ttk.Button(text='Add texts...',width=12,command=self.__command_AddTexts)
        self.btn_AddTexts.place(x=70,y=50)

        self.btn_DeleteCorpus = ttk.Button(text='Delete',width=6,command=self.__action_delete_corpus)
        self.btn_DeleteCorpus.place(x=175,y=50)
        
        self.btn_Workspace = ttk.Button(text='Workspace...',command=self.__action_select_workspace)
        self.btn_Workspace.place(x=175,y=25)
        # tools
        self.lbl_Tools = ttk.Label(self,text='Tools')
        self.lbl_Tools.place(x=10,y=90)
        self.lst_Tools = Listbox(self,width=24,height=15)
        #self.lst_Tools.bind('<<ListboxSelect>>',self.__action_get_selected_tool)
        self.lst_Tools['selectmode'] = 'single'
        self.lst_Tools.insert(1,'- Wordlist')
        self.lst_Tools.insert(2,'- Keywords')
        self.lst_Tools.insert(3,'- KWIC')
        self.lst_Tools.insert(4,'- Concordance')
        self.lst_Tools.insert(5,'- Collocates')
        self.lst_Tools.insert(6,'- N-grams')
        self.lst_Tools.place(x=10,y=110)
        self.lst_Tools.bind('<Double-Button-1>', self.__action_open_selected_tool)
        self.btn_Run = ttk.Button(self,text='Run',width=6)
        self.btn_Run.place(x=10,y=300)
        self.btn_Stop = ttk.Button(self,text='Stop',width=6)
        self.btn_Stop.place(x=70,y=300)
        self.btn_Options = ttk.Button(self,text='Opt',width=6)
        self.btn_Options.place(x=130,y=300)
        # 


        self.btn_Test = Button(self,text='Test',command=self.start_submit_thread)
        self.btn_Test.place(x=10,y=500) 

        self.btn_Stop = Button(self,text='Stop',command=self.__stop)
        self.btn_Stop.place(x=70,y=500)


        self.pgb_Progress = ttk.Progressbar(self, mode='indeterminate')
        self.pgb_Progress.place(x=10,y=550)


        self.lbl_Progress = ttk.Label(self, text='progress')
        self.lbl_Progress.place(x=10,y=570)
        # load corpora
        self.__load_corpora()

        # forms to avoid many instances
        self.frm_newcorpus = None
    

    def update_corpora(self,event=None):
        self.__load_corpora()

    def __load_corpora(self,event=None):
        if self.config['workspace'] != 'None':
            corpora = []
            folders = os.listdir(self.config['workspace'])
            for folder in folders:
                if os.path.exists(self.config['workspace'] + '/' + folder):
                    if os.path.isdir(self.config['workspace'] + '/' + folder):
                        corpora.append(folder)
            self.cmb_Corpus['values'] = corpora 
            self.cmb_Corpus.update()


    def __load_config(self):
        self.config = {}
        with open(self.__path + '/config.ini','rb') as fh:
            self.config = pickle.load(fh)
    
    def __save_current_config(self):
        with open(self.__path + '/config.ini','wb') as fh:
            pickle.dump(self.config,fh)
    
    def __save_default_config(self):
        self.config = {}
        self.config['workspace'] = 'None'
        self.config['corpus'] = 'None'
        with open(self.__path + '/config.ini','wb') as fh:
            pickle.dump(self.config,fh)
    
    def __check_config_file(self):
        if os.path.exists(self.__path + '/config.ini') == False:
            self.__save_default_config()
            self.__load_config()
        else:
            self.__load_config()
    
    
    def __about(self):
        message = 'Kitconc ' + kitconc.__version__
        message += '\n\njlopes@usp.br'
        message += '\n\nhttp://ilexis.net.br'
        messagebox.showinfo ('About...',message)
    

    def submit(self):
        self.__make()
    
    def start_submit_thread(self,event=None):
        self.submit_thread = Process (target=self.submit)
        self.submit_thread.daemon = True
        self.pgb_Progress['mode'] = 'indeterminate'
        self.pgb_Progress.start()
        self.submit_thread.start()
        self.after(20, self.check_submit_thread)
    
    def check_submit_thread(self):
        if self.submit_thread.is_alive():
            self.after(20, self.check_submit_thread)
        else:
            self.pgb_Progress.stop()
            self.pgb_Progress['mode'] = 'determinate'

    
    def __make (self):
        workspace = self.config['workspace']
        corpus_name = self.config['corpus']
        corpus = Corpus(workspace,corpus_name)
        wordlist = corpus.wordlist(show_progress=True)
        wordlist.save_excel(corpus.output_path + '/wordlist.xlsx')
        
    
    def __stop(self,event=None):
        self.submit_thread.terminate()
        self.lbl_Progress['text'] = 'Finished!'
    

    def __action_select_workspace(self,event=None):
        if self.config['workspace'] != 'None':
            folder = filedialog.askdirectory(title='Select workspace',initialdir=self.config['workspace'])
        else:
            folder = filedialog.askdirectory(title='Select workspace')

        if len(folder) != 0:
            if os.path.exists(folder):
                if os.path.isdir(folder):
                    self.config['workspace'] = folder 
                    self.__save_current_config()
    
    def __action_select_corpus(self,event=None):
        corpus = self.cmb_Corpus.get()
        self.config['corpus'] = corpus 
    

    def __command_new_corpus(self,corpus_name,language,encoding,foldername):
        self.submit_thread = Process (target=lambda:self.__action_add_new_corpus(corpus_name,language,encoding,foldername))
        self.submit_thread.daemon = True
        self.pgb_Progress['mode'] = 'indeterminate'
        self.pgb_Progress.start()
        self.submit_thread.start()
        self.after(20, self.__check_new_corpus)
    
    def __check_new_corpus(self):
        if self.submit_thread.is_alive():
            self.after(20, self.__check_new_corpus)
        else:
            self.pgb_Progress.stop()
            self.pgb_Progress['mode'] = 'determinate'
            self.__load_corpora()

    def __action_new_corpus(self,event=None):
        corpus_name = simpledialog.askstring('New corpus - step  1','Corpus name',initialvalue='mycorpus')
        if corpus_name != None:
            corpus_name = corpus_name.replace(' ','_')
            corpus_name = corpus_name.strip()
            corpus_language = simpledialog.askstring('New corpus - step 2','Language (english, portuguese)',initialvalue='english')
            if corpus_language != None:
                encoding =  simpledialog.askstring('New corpus - step 3','Encoding (utf-8, latin-1)',initialvalue='utf-8')
                if encoding != None:
                    if self.config['workspace'] != None:
                        folder = filedialog.askdirectory(title='New corpus - step 4',initialdir=self.config['workspace'])
                    else:
                        folder = filedialog.askdirectory(title='New corpus - step 4')
                    if os.path.exists(folder) == True:
                        foldername = folder 
                    if corpus_name != 'None':
                        self.__command_new_corpus(corpus_name,corpus_language,encoding,foldername)

                        
    
    def __action_add_new_corpus(self,corpus_name,language,encoding,foldername):
        workspace = self.config['workspace']
        corpus = Corpus(workspace,corpus_name,language=language,encoding=encoding)
        corpus.add_texts(foldername,show_progress=True)
    
    def __action_delete_corpus(self):
        message = "Are you sure you want to delete the corpus?"
        answer = messagebox.askyesno(title='Confirm',message=message)
        if answer == True:
            corpus = self.cmb_Corpus.get()
            workspace = self.config['workspace']
            if os.path.exists(workspace + '/' + corpus):
                shutil.rmtree(workspace + '/' + corpus)
                self.__load_corpora()
                self.cmb_Corpus.set('')
            
    def __action_open_selected_tool(self,event=None):
        corpus = self.cmb_Corpus.get()
        if len(corpus) != 0:
            selected_tool = self.lst_Tools.get(ACTIVE)
            selected_tool = selected_tool.replace('- ','')
            if selected_tool == 'Wordlist':
                frm = frmWordlist(master = self,config=self.config)
        else:
            message = 'You need to select a corpus to proceed.'
            messagebox.showinfo(title='Information', message=message)
    
    # Add texts

    def __command_AddTexts(self,event=None):
        if self.config['workspace'] != 'None' and self.config['corpus']!='None':
            folder = filedialog.askdirectory(title='Select folder',initialdir=self.config['workspace'])
            if os.path.exists(folder) == True:
                self.process = Process(target=lambda:self.__process_Start_AddTexts(folder))
                self.process.daemon = True 
                self.pgb_Progress['mode'] = 'indeterminate'
                self.pgb_Progress.start()
                self.process.start()
                self.after(20, self.__process_Check_AddTexts)
            else:
                messagebox.showwarning('Attention!',message='You need to select a valid folder path.')
        else:
            messagebox.showwarning('Attention!',message='You need to seletect a corpus to proceed.')

    def __process_Start_AddTexts(self,folder):
        workspace = self.config['workspace']
        corpus_name = self.config['corpus']
        corpus = Corpus(workspace,corpus_name)
        corpus.add_texts(folder,show_progress=True)

    def __process_Check_AddTexts(self,event=None):
        if self.process.is_alive():
            self.after(20, self.__process_Check_AddTexts)
        else:
            self.pgb_Progress.stop()
            self.pgb_Progress['mode'] = 'determinate'
            messagebox.showinfo('Success!',message='The texts were added to the corpus.')
            
         
    
    # New corpus
    def __new_corpus(self,event=None):
        for child in self.winfo_children():
            if type(child) is Toplevel:
                child.destroy()
        frm = frmNewCorpus(master=self)
    
    def close_TopLevel(self):
        for child in self.winfo_children():
            if type(child) is Toplevel:
                child.destroy()



    
    def run(self):
        while self.running == True:
            self.update()
            time.sleep(0.1)

        
    

