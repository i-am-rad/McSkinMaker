import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
from pathlib import Path
import shutil
import os
import uuid
# This program is copyright of ©Jacob Radcliffe
# https://github.com/i-am-rad
# All mentions of "Minecraft" are copyright and trademark of Microsoft
# The intent of this program is to teach and explain how Python can be used to solve simple problems.
# This program takes a Minecraft PNG image designed on Tynker, or other sites, and converts it to a mcpack file
# ***GPL3 LICENSING***
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details. You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

# create the GUI window - everywhere you see "gui" is a modification of the GUI
gui = tk.Tk()

# Title of Our Program
gui.title('McSkinMaker')

# Dimensions and Colors of Our GUI
gui.resizable(False, False)
gui.geometry('600x400')
gui['bg'] = '#DAF7A6'
Label(gui, text=f'McSkinMaker - Convert PNG to mcpack. \n©Jacob Radcliffe, GPL3', pady=20, bg='#ffbf00').pack()

# set global file path variables
file_name = "blank"
original_file = "blank"
directory_path = "blank"
short_name = "blank"
new_name = "blank"
final_path = "blank"
skin_name = "blank"

# This creates our open button to open files
# lambda is used to chain together functions
open_button = ttk.Button(
    gui,
    text='Open a Minecraft Image File',
    command=lambda: [select_file(), check_if_blank()]
)

# Attaching the open button to the top-level gui window
open_button.pack(expand=True)


# this function lets us select a file with file dialog
# it modifies the blank global variables with the file path
def select_file():
    filetypes = (
        ('Minecraft PNG Image', '*.png'),
        ('All files', '*.*')
    )
    global file_name
    file_name = fd.askopenfilename(
        title='Open a Minecraft Image',
        initialdir='/',
        filetypes=filetypes
    )


def check_if_blank():
    if file_name == "":
        gui.destroy()
    else:
        path_function(file_name)
        rename_skin()


# Reusable function to display a filepath in different ways.
# This is important for Minecraft mcpack files because file names are used in various ways in the JSON and LANG files
def path_function(fp):
    global original_file
    original_file = os.path.abspath(fp)
    global directory_path
    directory_path = os.path.dirname(fp)
    global short_name
    short_name = os.path.basename(fp)
    global skin_name
    skin_name = Path(fp).stem


# Rename the file yes/no window. "if" which defaults to true is the "yes" button. "else" = false is the "no" button
def rename_skin():

    skin_msg = "Make sure your skin name is short!" + "\nSkin Name Is: " + skin_name + "\nRename it?"
    answer = messagebox.askyesno("Skin Name", skin_msg)
    if answer:
        response = "Type in a new skin name, then click Save"
        showinfo(
            title='Rename',
            message=response
        )
        rename_block()

    else:
        showinfo(
            title='Ready',
            message="Ready to Convert"
        )
        convert_button()


# Creates the typing entry block in the gui window.
def rename_block():
    entry1 = tk.Entry(gui)
    entry1.pack(pady=30)
    Label(gui, text=f'Type a New Skin Name', pady=20, bg='#ffbf00').pack()

    # Saves the new file name ONLY when the the save button gets pressed
    Button(
        gui,
        text="Save",
        padx=10,
        pady=5,
        command=lambda: [save_data(entry1.get()), rename_command()]
    ).pack()


# updates the global variable on GUI save button command
def save_data(nn):
    global new_name
    new_name = nn


# Updates the global variables with the new filepath and skin name
def rename_command():
    global original_file
    global skin_name
    rename_file = directory_path + "/" + new_name + ".png"
    os.rename(original_file, rename_file)
    original_file = rename_file
    skin_name = new_name
    Label(gui, text=f'Skin Renamed to: {new_name}. Ready to Convert!', pady=20, bg='#ffbf00').pack()
    convert_button()


# This function uses lambda to chain all the other functions to the convert button.
def convert_button():
    Button(
        gui,
        text="Convert to mcpack",
        padx=10,
        pady=5,
        command=lambda: [move_image(), skins_json(), manifest_json(), lang_file(), zip_skin()]
    ).pack()


# Creates a temporary folder with the name of the skin, then copies the PNG file into the folder
# The final path is used from here-on to properly house all the JSON and LANG files
def move_image():
    global final_path
    final_path = os.path.join(directory_path, skin_name)
    os.mkdir(final_path)
    shutil.copy(original_file, final_path)
    os.chdir(final_path)


# For simplicity purposes the original JSON file is dissected so variables can substitute in the skin name
# The python JSON library can be used to generate a much cleaner version of this
def manifest_json():
    # the UUID library is used here to generate a unique UUID for the skin in two different places
    uuid_1 = str(uuid.uuid4())
    uuid_2 = str(uuid.uuid4())

    t1 = "{\"format_version\":1,\"header\":{\"name\":"
    t2 = "\"" + skin_name + "\""
    t3 = ",\"uuid\":"
    t4 = "\"" + uuid_1 + "\""
    t5 = ",\"version\":[1,0,0]},\"modules\":[{\"type\":\"skin_pack\",\"uuid\":"
    t6 = "\"" + uuid_2 + "\""
    t7 = ",\"version\":[1,0,0]}]}"
    text = t1 + t2 + t3 + t4 + t5 + t6 + t7

    file = "manifest.json"
    manifest_path = os.path.join(final_path, file)

    m = open(manifest_path, "w+")

    # write it to the file
    m.writelines(text)
    m.close()


def skins_json():
    t1 = "{\"skins\":[{\"localization_name\":"
    t2 = "\"" + skin_name + "\""
    t3 = ",\"geometry\":\"geometry.humanoid.custom\",\"texture\":"
    t4 = "\"" + skin_name + ".png" + "\""
    t5 = ",\"type\":\"free\"}],\"serialize_name\":"
    t6 = t2
    t7 = ", \"localization_name\":"
    t8 = t2 + "}"

    text = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8

    file = "skins.json"
    skins_path = os.path.join(final_path, file)

    s = open(skins_path, "w+")

    # write it to the file
    s.writelines(text)
    s.close()


def lang_file():
    # make the texts folder and gives us a path for the file
    texts = "texts"
    texts_path = os.path.join(final_path, texts)
    os.mkdir(texts_path)
    lang_path = os.path.join(texts_path, "en_US.lang")
    # make the lang file
    lang = open(lang_path, "w+")
    lang_text = (
        "skinpack", ".", skin_name, "=", skin_name, "\n", "  ", "skin", ".", skin_name, ".", skin_name, " ", "name=",
        skin_name
    )
    # write it to the file
    lang.writelines(lang_text)
    lang.close()


# Minecraft files (mcpack, mcaddon, etc) are just renamed zip files. You can rename them to zip to view the files.
# We need to zip up the temporary folder with the name of the skin.
def zip_skin():
    # We change directory to where we want the store zip file (not in the final path temp folder)
    os.chdir(directory_path)

    # This simple python command lets us name the zip file (skin_name), choose the extension type (.zip)
    # and it lets us choose where the files to be zipped are located (final_path)
    shutil.make_archive(skin_name, 'zip', final_path)

    # renames the zip file to the mcpack file extension by using a few variables to store filenames/paths
    zip_name = skin_name + ".zip"
    mcpack_name = skin_name + ".mcpack"
    src = os.path.join(directory_path, zip_name)
    mcpack_location = os.path.join(directory_path, mcpack_name)
    os.rename(src, mcpack_location)

    # delete the temporary folder
    shutil.rmtree(final_path)

    # generates the final prompt gui box
    result = "McPack File Created!" + "\nLocation is: " + mcpack_location + "\nOpen it Now?"
    answer = messagebox.askyesno("Conversion Complete", result)
    if answer:
        os.startfile(mcpack_location)
        gui.destroy()
    else:
        gui.destroy()


# run the application
gui.mainloop()
