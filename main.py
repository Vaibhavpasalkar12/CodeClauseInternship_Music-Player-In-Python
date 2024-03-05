from tkinter import *
from tkinter import filedialog
import pygame
import os

root = Tk()
root.title('Music Player')
root.geometry("500x350")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song_index = -1
paused = False

def load_music():
    global current_song_index
    root.directory = filedialog.askdirectory()
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert(END, song)

    if songs:
        current_song_index = 0
        songlist.selection_set(current_song_index)
        play_music()

def play_music():
    global paused, current_song_index

    if current_song_index == -1:
        return

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, songs[current_song_index]))
        pygame.mixer.music.play()

        update_current_song_label()  

        def play_next(event):
            next_music()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        root.bind("<MusicEnd>", play_next)
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song_index
    if current_song_index < len(songs) - 1:
        current_song_index += 1
    else:
        current_song_index = 0
    play_music()
    update_listbox()

def prev_music():
    global current_song_index
    if current_song_index > 0:
        current_song_index -= 1
    else:
        current_song_index = len(songs) - 1
    play_music()
    update_listbox()

def update_listbox():
    songlist.selection_clear(0, END)
    songlist.selection_set(current_song_index)
    songlist.activate(current_song_index)

def update_current_song_label():
    current_song_label.config(text="Currently Playing: " + songs[current_song_index])

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

songlist = Listbox(root, bg="black", fg="white", width=100, height=10)
songlist.pack()

play_btn_image  = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image  = PhotoImage(file='next.png')
prev_btn_image  = PhotoImage(file='previous.png')

control_frame = Frame(root)
control_frame.pack()

current_song_label = Label(root, font=("Helvetica", 12))
current_song_label.pack()

play_btn  = Button(control_frame, image=play_btn_image,  borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn  = Button(control_frame, image=next_btn_image,  borderwidth=0, command=next_music)
prev_btn  = Button(control_frame, image=prev_btn_image,  borderwidth=0, command=prev_music)

play_btn.grid (row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid (row=0, column=3, padx=7, pady=10)
prev_btn.grid (row=0, column=0, padx=7, pady=10)

root.mainloop()
