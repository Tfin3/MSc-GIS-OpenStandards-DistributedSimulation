
import tkinter as tk
from tkinter import filedialog

def CDB_Folderselector():
    CDBFolder.set(tk.filedialog.askdirectory())

def check_TMS_path():
    #Add function to check url and get valid xml
    return

root = tk.Tk()
root.title("Terrain Sample extraction tool")

tk.Label(root, text="Please enter bounding box for area of interest.") \
    .grid(row=0, column=0, columnspan=5, padx=5, pady=5)

tk.Label(root, text="Upper Left Lat") \
    .grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Upper Left Long") \
    .grid(row=1, column=1, padx=5, pady=5)
tk.Label(root, text="Lower Right Lat") \
    .grid(row=1, column=2, padx=5, pady=5)
tk.Label(root, text="Lower Right Long") \
    .grid(row=1, column=3, padx=5, pady=5)

ULLat = tk.StringVar(root,"")
ULLong = tk.StringVar(root, "")
LRLat = tk.StringVar(root,"")
LRLong = tk.StringVar(root, "")

tk.Entry(root, textvariable=ULLat, width=20, justify=tk.RIGHT) \
    .grid(row=2, column=0, columnspan=1, padx=5, pady=5)
tk.Entry(root, textvariable=ULLong, width=20, justify=tk.RIGHT) \
    .grid(row=2, column=1, columnspan=1, padx=5, pady=5)
tk.Entry(root, textvariable=LRLat, width=20, justify=tk.RIGHT) \
    .grid(row=2, column=2, columnspan=1, padx=5, pady=5)
tk.Entry(root, textvariable=LRLong, width=20, justify=tk.RIGHT) \
    .grid(row=2, column=3, columnspan=1, padx=5, pady=5)

#TODO Make some functions and link them to this GUI


tk.Label(root, text="Please choose the terrain database format") \
    .grid(row=5, column=0, columnspan=5, padx=5, pady=5)

CDBFolder = tk.StringVar(root, value="CDB Folder path here")

tk.Entry(root, textvariable=CDBFolder, width=60, justify=tk.RIGHT) \
    .grid(row=6, column=1, columnspan=4, padx=5, pady=5)

tk.Button(root, text="CDB Selection", command=CDB_Folderselector) \
    .grid(row=6, column=0, padx=5, pady=5)

TMSPath = tk.StringVar(root, value="http://insertTMS.com/layer/1.0.0/")

tk.Button(root, text="Check TMS Path", command=check_TMS_path) \
    .grid(row=7, column=0, padx=5, pady=5)

tk.Entry(root, textvariable=TMSPath, width=60, justify=tk.RIGHT) \
    .grid(row=7, column=1, columnspan=4, padx=5, pady=5)


root.mainloop()
