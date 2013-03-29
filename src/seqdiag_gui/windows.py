# Copyright (C) 2013 Luis Osa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import cStringIO

import wx
import wx.html

import seqdiagrams

HELP_PAGE = "var/resources/doc/help_page.html"
START_DIAG = """diagram {
  browser  -> webserver [label = "GET /index.html"];
  browser <-- webserver;
  browser  -> webserver [label = "POST /blog/comment"];
              webserver  -> database [label = "INSERT comment"];
              webserver <-- database;
  browser <-- webserver;
}
"""


class MainWindow(wx.Frame):
    """
    The MainWindow consists of two parts: a lower part where the user can type
    a text, and an upper part where the result of evaluating this text with
    seqdiag is presented. The menu allows to save the result as a graph file.
    """

    def __init__(self, filename='simple.diag', imgfile='simple.png'):
        super(MainWindow, self).__init__(None, size=wx.DefaultSize)
        self.filename = filename
        self.imgfile = imgfile
        self.dirname = '.'
        self.height = 0
        self.width = 0

        panel = wx.Panel(self, -1)
        self.status_bar = None
        self.save_button = None
        self.eval_button = None
        self.control = None
        self.img = None
        self.create_interior_widgets(panel)

        self.sizer = self.__arrange_boxes()
        panel.SetSizer(self.sizer)
        self.sizer.Fit(panel)
        self.Fit()

    def __arrange_boxes(self):
        """Arranges the lower and upper parts of the main window into a
        vertical stack"""
        proportion = 0
        text_proportion = 1
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.img, proportion, wx.EXPAND)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.AddStretchSpacer()
        buttons.Add(self.save_button, proportion, wx.ALIGN_LEFT)
        buttons.Add(self.eval_button, proportion, wx.ALIGN_RIGHT)
        buttons.AddStretchSpacer()
        box.Add(buttons, proportion, wx.EXPAND)
        box.Add((-1, 10))
        box.Add(self.control, text_proportion, wx.EXPAND | wx.ALL, 10)
        return box

    def create_interior_widgets(self, panel):
        """Creates interior window components, i.e. everything except status
        and menu bars."""
        self.control = wx.TextCtrl(
            panel, -1, START_DIAG, style=wx.TE_MULTILINE | wx.EXPAND)
        self.save_button = wx.Button(panel, wx.ID_SAVE)
        self.eval_button = wx.Button(panel, label='Evaluate')
        ## TODO: refactor into Model method ?
        png = seqdiagrams.diagram2png(
            seqdiagrams.text2diagram(self.control.GetValue()))
        stream = wx.InputStream(cStringIO.StringIO(png))
        png = wx.ImageFromStream(stream)
        self.width = png.GetWidth()
        self.height = png.GetHeight()
        self.img = wx.StaticBitmap(
            panel, -1, png.ConvertToBitmap(), (self.width, self.height))


class HtmlWindow(wx.html.HtmlWindow):
    """HtmlWindow as seen in the WxPython wiki:
       http://wiki.wxpython.org/wxPython%20by%20Example"""

    def __init__(self, parent, id):
        wx.html.HtmlWindow.__init__(self, parent, id)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())


class DocWindow(wx.Dialog):
    """DocWindow is a dialog that holds documentation about this application"""
    def __init__(self):
        wx.Dialog.__init__(self, None, -1,
                           "Seqdiag GUI documentation",
                           style=wx.DEFAULT_DIALOG_STYLE |
                           wx.THICK_FRAME |
                           wx.RESIZE_BORDER |
                           wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, wx.ID_ANY)
        htmlText = open(HELP_PAGE).read()
        hwin.SetPage(htmlText)
