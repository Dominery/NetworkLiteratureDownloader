import math
from collections import deque
import wx
from threading import Thread

from Downloader.download import Download
from Downloader.settings import Settings


def message_box(msg, title, yes_handler=None, no_handler=None):
    message_box = wx.MessageDialog(None, msg, title,
                                   wx.YES_NO | wx.ICON_QUESTION)
    choice = message_box.ShowModal()
    if choice == wx.ID_YES and yes_handler:
        yes_handler()
    if choice == wx.ID_NO and no_handler:
        no_handler()
    message_box.Destroy()


class DownloadInfo(wx.StaticBoxSizer):
    def __init__(self, panel):
        download_box = wx.StaticBox(parent=panel, label='DownloadInfo')
        super(DownloadInfo, self).__init__(download_box, wx.VERTICAL)
        self.download_process_gauge = wx.Gauge(parent=panel,style=wx.GA_HORIZONTAL | wx.GA_SMOOTH | wx.GA_TEXT,
                                               size=wx.DefaultSize, pos=wx.DefaultPosition, name='download_process',
                                               validator=wx.DefaultValidator, range=100)
        self.show_download_files_text = wx.TextCtrl(parent=panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.Add(self.download_process_gauge, proportion=1, flag=wx.ALL | wx.SHAPED, border=10)
        self.Add(self.show_download_files_text, proportion=4, flag=wx.ALL | wx.EXPAND, border=30)

    def show_info(self, process, download_files):
        self.download_process_gauge.SetValue(process)
        if download_files:
            show_article_info = '已下载完：' + download_files.pop() + '......\n'
            self.show_download_files_text.AppendText(show_article_info)

    def reset(self):
        self.download_process_gauge.SetValue(0)
        self.show_download_files_text.SetValue('')


class DownloadFrame(wx.Frame):

    def __init__(self, settings):
        self.settings = settings
        super().__init__(parent=None, size=self.settings.window_size, title=self.settings.window_title)
        self.Center()
        self.thread = deque(maxlen=5)
        self.panel = wx.Panel(parent=self)
        self.download_info = DownloadInfo(self.panel)
        self.file_button = wx.Button(parent=self.panel, label='file', id=3)
        self.download_button = wx.Button(parent=self.panel, label='Download', id=2)
        self.search_text = wx.TextCtrl(parent=self.panel,id=1,style=wx.TE_PROCESS_ENTER)
        # wx.TE_PROCESS_ENTER produce a event when user press enter
        self.choice_box = wx.Choice(parent=self.panel, choices=[])
        self.timer = wx.Timer(self)
        self.set_up()

    def set_up(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.file_button, proportion=1, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        hbox.Add(self.search_text, proportion=2, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        hbox.Add(self.choice_box, proportion=4, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        hbox.Add(self.download_button, proportion=1, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        vbox.Add(hbox, proportion=1, flag=wx.ALL | wx.EXPAND)
        vbox.Add(self.download_info, proportion=4, flag=wx.CENTER | wx.EXPAND)
        self.panel.SetSizer(vbox)
        self.bind_event()

    def bind_event(self):
        self.Bind(wx.EVT_TEXT_ENTER, self.search_onclick, self.search_text)
        self.Bind(wx.EVT_BUTTON, self.download_onclick, id=2)
        self.Bind(wx.EVT_BUTTON, self.choose_directory, id=3)
        self.Bind(wx.EVT_TIMER, self.show_download_info, self.timer)

    def search_onclick(self, event):
        book = self.search_text.GetValue()
        if book:
            self.download = Download(book, self.settings)
            self.download.search_related_book()
            choices = ['《' + i.title + '》' + i.author for i in self.settings.choose_urls][0:self.settings.select_max]
            self.choice_box.SetItems(choices)
        else:
            return

    def reset(self):
        self.settings.reset()
        self.search_text.SetValue('')
        self.choice_box.SetItems([])
        self.download_button.Enable()
        self.thread.popleft()
        self.download_info.reset()

    def download_onclick(self, event):
        select = self.choice_box.GetSelection()
        if select >= 0:
            if not self.settings.store_directory_path:
                message_box("choose a directory to store", "WARNING!", self.choose_directory)
            if self.settings.store_directory_path:
                self.download.get_article_urls(select)
                self.download.mkdir(self.settings.store_directory_path)
                self.thread.append(Thread(target=self.download.download))
                self.thread[-1].start()
                event.GetEventObject().Disable()
                self.timer.Start(100)

    def show_download_info(self, event):
        if bool(self.settings.completed_article) or self.settings.process < self.settings.sum_tasks:
            process = math.floor(self.settings.process*100/self.settings.sum_tasks+0.5)
            self.download_info.show_info(process,self.settings.completed_article)
        else:
            self.timer.Stop()
            message_box("the downloading task is completed,do you want to continue a new task?", "COMPLETED",
                        self.reset, self.Close)

    def choose_directory(self, event=None):
        dialog = wx.DirDialog(None, "choose a directory:",
                              style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.settings.store_directory_path = dialog.GetPath()
        dialog.Destroy()


class App(wx.App):
    def OnInit(self):
        settings = Settings()
        frame = DownloadFrame(settings)
        frame.Show()
        return True


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
