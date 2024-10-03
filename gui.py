import tkinter as tk
import ttkbootstrap as ttk
import threading
import pyperclip
from scrapper import Process

# window = tk.Tk()
window = ttk.Window() 
# font='Calibri 24 bold')

window.title('Tiktok Video Extractor')
window.geometry('1000x600')
window.iconbitmap('iconjpg.ico')
# window.configure(borderwidth="1")
window.configure(relief="sunken")
window.configure(background="#838485")
window.configure(cursor="arrow")
window.configure(highlightbackground="#838485")
window.configure(highlightcolor="black")

#----input field------------
input_frame = ttk.Frame(master=window)

acc_name = ttk.Label(master=input_frame, text='Account name :   ')
account_name_str = tk.StringVar()
account_name = ttk.Entry(master=input_frame, textvariable=account_name_str)

no_vid = ttk.Label(master=input_frame, text='No. of Videos :    ')
no_of_videos = tk.IntVar()
videos = ttk.Entry(master=input_frame, textvariable=no_of_videos)

style = ttk.Style()
style.configure('TButton', width=30, height=30)

status_label = tk.Label(window, text="", font=("Helvetica", 10, "bold"))
#------------------------------------------------------------------
data = None
#----Table Data--------------------------------------------------
def table(data):
    scrollbar = ttk.Scrollbar(window, orient="vertical")
    print(data)
    tree = ttk.Treeview(window, columns=('S.no','Title', 'Video Link'), show='headings', yscrollcommand=scrollbar.set)
    tree.heading('#0', text='')
    tree.heading('S.no', text='S.no')
    tree.heading('Title', text='Title')
    tree.heading('Video Link', text='Video Link')

    tree.column('#0', width=5)
    tree.column('S.no', width=60)
    tree.column('Title', width=300)
    tree.column('Video Link', width=500)

    scrollbar.config(command=tree.yview)

    k = 0
    for i, j  in zip(data['title'], data['link']):
        k += 1
        tree.insert('', 'end', values=(k, i, j))

    scrollbar.pack(side='right', fill='y')
    tree.pack(side='left', fill='both', expand=True)

    
class Functions:
    """ Functionality of our FrontEnd
    """
    def __init__(self):
        self.scraper = None
        self.data = None
        
    def table(self):
        table(self.data)
        
    def generate(self):
        """ Generating Links by loading loading account and collecting links
        """
        status_label.config(text="Link Generation has been started...")
        accName = account_name_str.get()
        links = no_of_videos.get()
        self.scraper = Process()
        subprocess = self.scraper.process(str(accName), int(links))
        self.data = self.scraper.data
        status_label.config(text="Done...")
#         self.table()
        
    def download(self):
        status_label.config(text="Downloading has been started...")
        self.scraper.downloader()
        status_label.config(text="Done...")

    def rename(self):
        self.scraper.rename()
        status_label.config(text="Renaming Done.")

#------------------------------------------------------------------
f = Functions() 
generate = ttk.Button(master=input_frame, text='Generate', style='TButton', command=threading.Thread(target=f.generate).start)
show_table = ttk.Button(master=input_frame, text='Display Data', style='TButton', command=threading.Thread(target=f.table).start)
download = ttk.Button(master=input_frame, text='Download', style='TButton', command=threading.Thread(target=f.download).start)
button = ttk.Button(master=input_frame, text='Rename', style='TButton', command=threading.Thread(target=f.rename).start)

acc_name.grid(row=3, column=0)
account_name.grid(row=3, column=1, columnspan=3, sticky="ew")

no_vid.grid(row=5, column=0)
videos.grid(row=5, column=1, columnspan=3, sticky="ew")

generate.grid(row=6, column=0)
show_table.grid(row=6, column=1)
download.grid(row=6, column=2)
button.grid(row=6, column=3)

input_frame.config(width=100, height=500)
input_frame.pack(pady = 10, side="top")

# # Change the text color (foreground)
status_label.config(foreground="white")

# # Change the background color
status_label.config(background="#838485")

status_label.pack(after=input_frame)

def check_events():
    window.update()  # Update the Tkinter event loop
    window.after(100, check_events)

check_events()
    
window.mainloop()