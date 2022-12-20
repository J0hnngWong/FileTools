from tkinter import *
from tkinter import ttk
import tkinter
from same_file_filter import SameFileFilter

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

text_placeholder = Variable(name='text_placeholder', value='')
top_label = ttk.Label(frm, text='Hello World!')
processing_file_label = ttk.Label(frm, text='None')
file_list = tkinter.Listbox(frm, height=5)
file_tree = ttk.Treeview(frm, height=10)
entry = ttk.Entry(frm, width=20, textvariable=text_placeholder)
quit_button = ttk.Button(frm, text='Quit', command=root.destroy)

def processing_file(file_name: str):
    processing_file_label.configure(text=file_name)

def check_entry():
    entry_text = entry.get()
    top_label.configure(text=entry_text)
    file_filter = SameFileFilter()
    file_filter.set_process_handler(handler=processing_file)
    file_filter.check_have_same_file(dir_path=entry_text)
    file_filter.file_md5_dict
    file_list_str = ''
    for key in file_filter.file_md5_dict:
        file_path_list = file_filter.file_md5_dict[key]
        for file_path in file_path_list:
            file_list_str = f'{file_list_str} {file_path}'
    list_var = StringVar(name='name', value=file_list_str)
    file_list.configure(listvariable=list_var)

check_button = ttk.Button(frm, text='Check', command=check_entry)

view_list: list[Grid] = [
    top_label,
    processing_file_label,
    file_list,
    entry,
    check_button,
    quit_button
]

for index in range(len(view_list)):
    view = view_list[index]
    view.grid(column=0, row=index)

root.mainloop()
