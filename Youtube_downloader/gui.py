from pytube import YouTube
from tkinter import filedialog, Tk, StringVar
from tkinter import ttk
from tkinter import *
import tkinter
import re
import threading


class Application:
    choicevar: StringVar

    def __init__(self, root):

        self.root = root
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.config(bg='#ffdddd')

        top_label = Label(self.root, text="youtube downloader User Interface", fg="red", font=("Tyoe zero", 70))
        top_label.grid(pady=(0, 20))

        link_label = Label(self.root, text='Enter  this link here')
        link_label.grid(pady=(0, 20))

        self.youtubeEntryVar = StringVar()
        self.youtubeEntry = Entry(self.root, width=70, textvariable=self.youtubeEntryVar)
        self.youtubeEntry.grid(pady=(0, 15), ipady=2)

        self.youtubeEntryError = Label(self.root, text='')
        self.youtubeEntryError.grid(pady=(0, 0))

        self.youtubeFileSaveLabel = Label(self.root, text="Choose File Directory")
        self.youtubeFileSaveLabel.grid()

        self.youtubeFileDirectoryButton = Button(self.root, text="Directory", command=self.openDirectory)
        self.youtubeFileDirectoryButton.grid(pady=(10, 3))

        self.fileLocationLabel = Label(self.root, text="")
        self.fileLocationLabel.grid()

        self.youtubeChooselabel = Label(self.root, text='choose download type')
        self.youtubeChooselabel.grid()

        self.downloadChoices = [('Audio MP3', 1), ('Video MP4', 2)]

        self.choicevar = StringVar()
        self.choicevar.set(1)

        for text, mode in self.downloadChoices:
            self.youtubeChoices = Radiobutton(self.root, text=text, variable=self.choicevar, value=mode)
            self.youtubeChoices.grid()

        self.downloadButton = Button(self.root, text="Download File", command=self.checkyoutubelink)
        self.downloadButton.grid()

    def checkyoutubelink(self):

        self.matchyoutubelink = re.match("^https://www.youtube.com/", self.youtubeEntryVar.get())
        if not self.matchyoutubelink:
            self.youtubeEntryError.config(text="This Link is Invalid link", fg='red')

        elif not self.openDirectory:
            self.fileLocationLabel.config(text="Choose a Directory", fg='red')

        elif self.matchyoutubelink and self.openDirectory:
            self.downloadwindow()

    def downloadwindow(self):
        self.newwindow = Toplevel(self.root)
        self.root.withdraw()
        self.newwindow.state('zoomed')
        self.newwindow.grid_rowconfigure(0, weight=0)
        self.newwindow.grid_columnconfigure(0, weight=1)

        self.app = Secondapp(self.newwindow, self.youtubeEntryVar.get(), self.Foldername, self.choicevar.get())

    def openDirectory(self):
        self.Foldername = filedialog.askdirectory()

        if len(self.Foldername) > 0:
            self.fileLocationLabel.config(text=self.Foldername)
            return True

        else:
            self.fileLocationLabel.config(text='Please choose a Directory')


class Secondapp:
    def __init__(self, downloadWindow, youtubelink, Foldername, choices):
        self.downloadWindow = downloadWindow
        self.youtubelink = youtubelink
        self.Foldername = Foldername
        self.choices = choices

        self.yt = YouTube(self.youtubelink)

        if choices == '1':
            self.video_type = self.yt.streams.filter(only_audio=True).first()
            self.MaxFilesize = self.video_type.filesize
        if choices == '2':
            self.video_type = self.yt.streams.first()
            self.MaxFilesize = self.video_type.filesize

        self.loadingLabel = Label(self.downloadWindow, text='Downloading file in progress')
        self.loadingLabel.grid(pady=(100, 0))

        self.loadingPercent = Label(self.downloadWindow, text='0', fg='green')
        self.loadingPercent.grid(pady=(50, 0))

        self.progressBar = ttk.Progressbar(self.downloadWindow, length=500, orient='horizontal', mode='indeterminate')
        self.progressBar.grid(pady=(50, 0))
        self.progressBar.start()

        threading.Thread(target=self.yt.register_on_progress_callback(self.show_progress)).start()

        threading.Thread(target=self.downloadFile).start()

    def downloadFile(self):
        if self.choices == '1':
            self.yt.streams.filter(only_audio=True).first().download(self.Foldername)

        if self.choices == '2':
            self.yt.streams.first().download(self.Foldername)

    def show_progress(self, streams=None, chunks=None, bytes_remaining=None):

        self.percentCount = float(f'{100 - (100 * (bytes_remaining / self.MaxFilesize)):0.2f}')

        if self.percentCount < 100:
            self.loadingPercent.config(text=self.percentCount)
        else:
            self.progressBar.stop()
            self.loadingLabel.grid_forget()
            self.progressBar.grid_forget()

            self.downloadFinished = Label(self.downloadWindow, text='Download file finished')
            self.downloadFinished.grid(pady=(150, 0))

            self.downloadfilename = Label(self.downloadWindow, text=self.yt.title)
            self.downloadfilename.grid(pady=(50, 0))

            MB = float(f'{self.MaxFilesize / 1000000:0.2f}')

            self.downloadFilesize = Label(self.downloadWindow, text=str(MB))
            self.downloadFilesize.grid(pady=(50, 0))


if __name__ == '__main__':
    window = Tk()
    window.title('Youtube Downloader')
    window.state("zoomed")
    app = Application(window)
    mainloop()
