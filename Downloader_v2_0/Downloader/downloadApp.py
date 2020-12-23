import os
from math import floor
from collections import deque
import wx
from threading import Thread

from Downloader.download import Download
from Downloader.settings import Settings
from Downloader.bookstats import BookStats


class Tasks:
    """
    using Singleton Design and observer pattern
    """
    _shared_dict = {}

    def __new__(cls, *args, **kwargs):
        instance = super(Tasks, cls).__new__(cls, *args, **kwargs)
        instance.__dict__ = cls._shared_dict
        return instance

    def __init__(self):
        if not self._shared_dict:
            self._tasks = deque(maxlen=10)
            self._observers = []

    def add_task(self, task):
        self._tasks.append(task)

    def recall_task(self):
        self._tasks.pop()

    def has_any_task(self):
        return bool(self._tasks)

    def full(self):
        return len(self._tasks) == self._tasks.maxlen

    def assignment(self):
        return self._tasks.popleft()

    @property
    def tasks_max(self):
        return self._tasks.maxlen

    def __iter__(self):
        return (task for task in self._tasks)

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_all(self):
        for observer in self._observers:
            observer.reset()


def message_box(msg, title, yes_handler=None, no_handler=None):
    message_box = wx.MessageDialog(None, msg, title,
                                   wx.YES_NO | wx.ICON_QUESTION)
    choice = message_box.ShowModal()
    if choice == wx.ID_YES and yes_handler:
        yes_handler()
    if choice == wx.ID_NO and no_handler:
        no_handler()
    message_box.Destroy()


def transparent(wx_class, *args, **kwargs):
    class Transparent(wx_class):
        def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
            wx_class.__init__(self, parent, id, label, pos, size, style, name)
            self.Bind(wx.EVT_PAINT, self.on_paint)
            self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
            self.Bind(wx.EVT_SIZE, self.on_size)

        def on_paint(self, event):  # 重写on_paint可以对控件进行重写重新构造形状
            bdc = wx.PaintDC(self)
            dc = wx.GCDC(bdc)
            font_face = self.GetFont()
            font_color = self.GetForegroundColour()
            dc.SetFont(font_face)
            dc.SetTextForeground(font_color)
            dc.DrawText(self.GetLabel(), 0, 0)

        def on_size(self, event):
            self.Refresh()
            event.Skip()

    return Transparent(*args, **kwargs)


class DownloadInfo(wx.StaticBoxSizer):
    def __init__(self, panel):
        download_box = transparent(wx.StaticBox, parent=panel, label='DownloadInfo')
        super(DownloadInfo, self).__init__(download_box, wx.VERTICAL)
        self.download_process_gauge = wx.Gauge(parent=panel, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH | wx.GA_TEXT,
                                               size=wx.DefaultSize, pos=wx.DefaultPosition, name='download_process',
                                               validator=wx.DefaultValidator, range=100)
        self.show_download_files_text = wx.TextCtrl(parent=panel, size=(200, 150),
                                                    style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE)
        self.show_process_label = transparent(wx.StaticText, parent=panel)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        grid.Add(self.download_process_gauge, pos=(0, 0), flag=wx.FIXED_MINSIZE)
        grid.Add(self.show_process_label, pos=(0, 1), flag=wx.SHAPED)
        grid.Add(self.show_download_files_text, pos=(1, 0), flag=wx.EXPAND)
        grid.AddGrowableCol(0)
        grid.AddGrowableRow(1)
        self.Add(grid)

    def show_info(self, process, download_files):
        self.download_process_gauge.SetValue(process)
        self.show_process_label.SetLabelText(str(process) + '%')
        if download_files:
            show_article_info = '已下载：' + download_files.pop() + '\n'
            self.show_download_files_text.AppendText(show_article_info)

    def reset(self):
        self.download_process_gauge.SetValue(0)
        self.show_download_files_text.SetValue('')
        self.show_process_label.SetLabelText('')


class DownloadTasks(wx.StaticBoxSizer):
    def __init__(self, panel):
        tasks_box = transparent(wx.StaticBox, parent=panel, label="Control Tasks")
        super(DownloadTasks, self).__init__(tasks_box, wx.VERTICAL)
        self.choice_box = wx.Choice(parent=panel, choices=[])
        self.recall_button = wx.Button(parent=panel, label='Recall', id=4)
        self.add_button = wx.Button(parent=panel, label='Add', id=5)
        self.tasks_info = wx.TextCtrl(parent=panel, size=(150, 113),
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE)
        grid = wx.GridBagSizer(vgap=5, hgap=5)
        grid.Add(self.choice_box, pos=(0, 0), span=(1, 2), flag=wx.CENTER | wx.EXPAND)
        grid.Add(self.add_button, pos=(1, 1), span=(1, 1), flag=wx.FIXED_MINSIZE | wx.CENTER)
        grid.Add(self.recall_button, pos=(1, 0), span=(1, 1), flag=wx.FIXED_MINSIZE | wx.CENTER)
        grid.Add(self.tasks_info, pos=(2, 0), span=(2, 2), flag=wx.EXPAND | wx.ALL)
        grid.AddGrowableRow(2)
        self.Add(grid)
        self.tasks = Tasks()
        self.tasks.add_observer(self)

    def reset(self):
        self.tasks_info.SetValue('')
        self.choice_box.SetItems([])
        self.add_button.Enable()
        self.recall_button.Enable()

    def disable(self):
        self.add_button.Disable()
        self.recall_button.Disable()

    def bind_event(self, frame):
        frame.Bind(wx.EVT_BUTTON, self.add_task, id=5)
        frame.Bind(wx.EVT_BUTTON, self.recall_task, id=4)

    def add_task(self, event):
        select = self.choice_box.GetSelection()
        if select >= 0:
            self.stats.book = self.stats.books_infos[select]
            if self.stats not in self.tasks:
                if self.tasks.full():
                    message_box(f'You can only add {self.tasks.tasks_max} tasks', 'WARNING!')
                else:
                    self.tasks_info.AppendText(f'《{self.stats.book.title}》' + '\n')
                    self.stats.get_article()
                    self.tasks.add_task(self.stats)
            self.choice_box.SetItems([])

    def recall_task(self, event):
        if self.tasks.has_any_task():
            self.tasks.recall_task()
            self.tasks_info.SetValue(''.join([f'《{i.book.title}》\n' for i in self.tasks]))

    def set_choices(self, book, settings):
        self.stats = BookStats(book, settings)
        self.stats.search()
        choices = ['《' + i.title + '》' + i.author for i in self.stats.books_infos][0:settings.select_max]
        self.choice_box.SetItems(choices)


class DownloadFrame(wx.Frame):

    def __init__(self, settings):
        self.settings = settings
        super().__init__(parent=None, title=self.settings.window_title)
        self.SetTransparent(self.settings.window_transparent)
        # self.SetBackgroundColour('blue')
        self.Center()
        self.panel = wx.Panel(parent=self)
        self.download_info = DownloadInfo(self.panel)
        self.file_button = wx.Button(parent=self.panel, label='file', id=3)
        self.download_task = DownloadTasks(self.panel)
        self.download_button = wx.Button(parent=self.panel, label='Download', id=2)
        self.search_text = wx.TextCtrl(parent=self.panel, id=1, style=wx.TE_PROCESS_ENTER)
        # wx.TE_PROCESS_ENTER produce a event when user press enter
        self.timer = wx.Timer(self)
        self.set_up()

    def set_up(self):
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        title = transparent(wx.StaticText, parent=self.panel, label='Downloader')
        title.SetFont(font)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(vgap=10, hgap=10)
        grid.Add(self.file_button, pos=(0, 0), span=wx.DefaultSpan, flag=wx.FIXED_MINSIZE | wx.CENTER, border=10)
        grid.Add(self.search_text, pos=(0, 1), span=(1, 2), flag=wx.CENTER | wx.EXPAND, border=10)
        grid.Add(self.download_button, pos=(0, 3), span=(1, 1), flag=wx.CENTER | wx.FIXED_MINSIZE)
        grid.Add(self.download_task, pos=(1, 3), span=(4, 2), flag=wx.EXPAND | wx.CENTER)
        grid.Add(self.download_info, pos=(1, 0), span=(4, 3), flag=wx.CENTER | wx.EXPAND)
        grid.AddGrowableRow(2)
        grid.AddGrowableCol(1)
        topSizer.Add(title, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(grid, 0, wx.EXPAND)
        self.panel.SetSizerAndFit(topSizer)
        self.SetSizeHints(420, 300, 490, 350)  # set min width height and max width and height
        self.bind_event()

    def bind_event(self):
        self.Bind(wx.EVT_TEXT_ENTER, self.search_onclick, self.search_text)
        self.Bind(wx.EVT_BUTTON, self.download_onclick, id=2)
        self.Bind(wx.EVT_BUTTON, self.choose_directory, id=3)
        self.Bind(wx.EVT_TIMER, self.show_download_info, self.timer)
        self.download_task.bind_event(self)
        if os.path.exists(self.settings.background_picture):
            self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def search_onclick(self, event):
        book = self.search_text.GetValue()
        if book:
            self.download_task.set_choices(book, self.settings)
        else:
            return

    def reset(self):
        self.download_button.Enable()
        self.search_text.SetValue('')

    def download_onclick(self, event):
        if not self.settings.store_directory_path:
            message_box("choose a directory to store", "WARNING!", self.choose_directory)
        self.tasks = Tasks()
        if self.settings.store_directory_path and self.tasks.has_any_task():
            self.current_task = self.tasks.assignment()
            event.GetEventObject().Disable()
            self.download_task.disable()
            self.tasks.add_observer(self)
            self.tasks.add_observer(self.download_info)
            self.start_task(self.current_task)

    def start_task(self, task):
        self.download_info.reset()
        downloader = Download(task, self.settings)
        downloader.mkdir()
        thread = Thread(target=downloader.download)
        thread.start()
        self.timer.Start(100)

    def show_download_info(self, event):
        if bool(self.current_task.completed_articles) or self.current_task.process < self.current_task.sum_tasks:
            process = floor(self.current_task.process * 100 / self.current_task.sum_tasks + 0.5)
            self.download_info.show_info(process, self.current_task.completed_articles)
        else:
            self.timer.Stop()
            if self.tasks.has_any_task():
                self.current_task = self.tasks.assignment()
                self.start_task(self.current_task)
            else:
                message_box("the downloading task is completed,do you want to continue a new task?", "COMPLETED",
                            self.tasks.notify_all, self.Close)

    def choose_directory(self, event=None):
        dialog = wx.DirDialog(None, "choose a directory:",
                              style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.settings.store_directory_path = dialog.GetPath()
        dialog.Destroy()

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap(self.settings.background_picture)
        dc.DrawBitmap(bmp, 0, 0)


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
