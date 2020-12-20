import wx
from threading import Thread

from Downloader_v1_0.download import Download
from Downloader_v1_0.settings import Settings


class DownloadFrame(wx.Frame):

    def __init__(self, settings):
        self.settings = settings
        super().__init__(parent=None, size=self.settings.window_size, title=self.settings.window_title)
        self.Center()
        self.choice_list = ['zhong']
        self.thread = []
        self.path = None
        self.panel = wx.Panel(parent=self)
        self.show_download_process_label = wx.StaticText(parent=self.panel, label='')
        self.show_download_files_label = wx.StaticText(parent=self.panel, label='', style=wx.TE_MULTILINE)
        self.file_button = wx.Button(parent=self.panel, label='file', id=3)
        self.search_button = wx.Button(parent=self.panel, label='Search', id=1)
        self.download_button = wx.Button(parent=self.panel, label='Download', id=2)
        self.search_text = wx.TextCtrl(parent=self.panel)
        self.choice_box = wx.Choice(parent=self.panel, choices=self.choice_list)
        self.timer = wx.Timer(self)
        self.set_up()

    def set_up(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.file_button, proportion=1, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        hbox.Add(self.search_text, proportion=4, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        hbox.Add(self.search_button, proportion=1, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        hbox.Add(self.choice_box, proportion=4, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        hbox.Add(self.download_button, proportion=1, flag=wx.FIXED_MINSIZE | wx.CENTER, border=30)
        vbox.Add(hbox, proportion=1, flag=wx.ALL | wx.EXPAND)
        download_info_box = wx.StaticBox(parent=self.panel, label='Download Info')
        hsbox = wx.StaticBoxSizer(download_info_box, wx.VERTICAL)
        hsbox.Add(self.show_download_process_label, proportion=1, flag=wx.ALL | wx.EXPAND, border=30)
        hsbox.Add(self.show_download_files_label, proportion=3, flag=wx.ALL | wx.EXPAND, border=30)
        vbox.Add(hsbox, proportion=4, flag=wx.CENTER | wx.EXPAND)
        self.panel.SetSizer(vbox)
        self.bind_event()
        self.show_download_files_label.SetLabelText('There will show you the downloaded articles...')
        self.show_download_process_label.SetLabelText('There will show you the progress of download')

    def bind_event(self):
        self.Bind(wx.EVT_BUTTON, self.search_onclick, id=1)
        self.Bind(wx.EVT_BUTTON, self.download_onclick, id=2)
        self.Bind(wx.EVT_BUTTON, self.choose_directory, id=3)
        self.Bind(wx.EVT_TIMER, self.show_download_info, self.timer)

    def search_onclick(self, event):
        book = self.search_text.GetValue()
        if book:
            self.download = Download(book, self.settings)
            self.download.search_related_book()
            choices = ['《' + i.title + '》' + i.author for i in self.settings.choose_urls][0:5]
            self.choice_box.SetItems(choices)
        else:
            return

    def download_onclick(self, event):
        select = self.choice_box.GetSelection()
        if select >= 0 :
            if not self.path:
                self.message_box()
                return
            self.download.get_article_urls(select)
            self.download.mkdir(self.path)
            self.thread.append(Thread(target=self.download.download))
            self.thread[-1].start()
            event.GetEventObject().Disable()
            self.timer.Start(500)
        else:
            return

    def show_download_info(self,event):
        if 0 < self.settings.process < self.settings.sum_tasks:
            self.show_download_process_label.SetLabelText(self.settings.format_process)
            self.show_download_files_label.SetLabelText('\n'.join(self.settings.completed_article))
        elif self.settings.process >= self.settings.sum_tasks:
            self.timer.Stop()
        else:
            return

    def choose_directory(self, event=None):
        dialog = wx.DirDialog(None, "choose a directory:",
                              style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
        dialog.Destroy()

    def message_box(self):
        message_box = wx.MessageDialog(None, "choose a directory to store", "WARNING!",
                                       wx.YES_NO | wx.ICON_QUESTION)
        if message_box.ShowModal() == wx.ID_YES:
            self.choose_directory()
        message_box.Destroy()


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
