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
import os.path
import cStringIO

import wx, wx.html

from seqdiagrams import text2diagram, diagram2png

HELP_PAGE = 'var/resources/doc/help_page.html'

class MainWindow(wx.Frame):
    """
    The MainWindow consists of two parts: a lower part where the user can type
    a text, and an upper part where the result of evaluating this text with
    seqdiag is presented. The menu allows to save the result as a graph file.
    """

    def __init__(self, filename='simple.diag', imgfile='simple.png'):
        super(MainWindow, self).__init__(None, size=wx.DefaultSize) #(400,200))
        self.filename = filename
        self.imgfile = imgfile
        self.dirname = '.'
        self.height = 0
        self.width = 0
        self.already_saved = False

        panel = wx.Panel(self, -1)
        self.status_bar = None
        self.save_button = None
        self.eval_button = None
        self.control = None
        self.img = None
        self.create_interior_widgets(panel)
        self.create_exterior_widgets()

        self.sizer = self.__arrange_boxes()
        panel.SetSizer(self.sizer)
        self.sizer.Fit(panel)
        self.Fit()

    def __arrange_boxes(self):
        """Arranges the lower and upper parts of the main window into a
        vertical stack"""
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.img, 0, wx.EXPAND)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.AddStretchSpacer()
        buttons.Add(self.save_button, 0, wx.ALIGN_LEFT)
        buttons.Add(self.eval_button, 0, wx.ALIGN_RIGHT)
        buttons.AddStretchSpacer()
        box.Add(buttons, 0, wx.EXPAND)
        box.AddF(self.control, wx.SizerFlags().Expand().Border(wx.ALL, 10))
        return box

    def create_interior_widgets(self, panel):
        """Creates interior window components, i.e. everything except status
        and menu bars."""
        fileh = open(self.filename, 'r')
        self.control = wx.TextCtrl(panel, -1, fileh.read(),
                                   style=wx.TE_MULTILINE)
        png = wx.Image(self.imgfile, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.width = png.GetWidth()
        self.height = png.GetHeight()
        self.img = wx.StaticBitmap(panel, -1, png,
                                   (self.width, self.height))
        self.save_button = wx.Button(panel, wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.on_save_button, self.save_button)
        self.eval_button = wx.Button(panel, label='Evaluate')
        self.Bind(wx.EVT_BUTTON, self.on_edit, self.eval_button)

    def create_exterior_widgets(self):
        """Creates exterior window components, such as menu and status bar."""
        self.create_menu()
        self.set_title()
        self.status_bar = self.CreateStatusBar()

    def create_menu(self):
        """Creates the main window menu"""
        file_menu = wx.Menu()
        for item_id, label, help_text, handler in \
            [(wx.ID_ABOUT, '&About', 'Information about this program',
                self.on_about),
             (wx.ID_OPEN, '&Open', 'Open a new file', self.on_open),
             (wx.ID_SAVE, '&Save', 'Save the current file', self.on_save),
             (wx.ID_SAVEAS, 'Save &As', 'Save the file under a different name',
                self.on_save_as),
             (None, None, None, None),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.on_exit)]:
            if item_id == None:
                file_menu.AppendSeparator()
            else:
                item = file_menu.Append(item_id, label, help_text)
                self.Bind(wx.EVT_MENU, handler, item)
        help_menu = wx.Menu()
        help_item = help_menu.Append(wx.ID_HELP, '&Documentation',
                'Help on this application')
        self.Bind(wx.EVT_MENU, self.on_help, help_item)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File') # Add the file_menu to the MenuBar
        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)  # Add the menu_bar to the Frame

    def set_title(self):
        """Sets the window title from the edited file"""
        super(MainWindow, self).SetTitle('Editing %s' % self.filename)

    # Helper methods:

    def default_file_dialog_options(self):
        """Returns a dictionary with file dialog options that can be
        used in both the save file dialog as well as in the open file
        dialog. """
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.*')

    def ask_user_for_filename(self, **dialogOptions):
        """Returns the success of asking the user, through a wx standard
        dialog, for a new filename to edit"""
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            filename_provided_by_user = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.set_title() # Update the window title with the new filename
        else:
            filename_provided_by_user = False
        dialog.Destroy()
        return filename_provided_by_user

    # Event handlers:

    def on_about(self, event):
        """Handles the event of clicking on the 'About' menu option"""
        del event
        desc = ("Seqdiag GUI is a a graphic user interface to Takeshi Komiya's "
                "simple sequence diagram package, called seqdiag")
        license = ("Seqdiag GUI is free software; you can redistribute "
                   "it and/or modify it under the terms of the GNU General "
                   "Public License as published by the Free Software "
                   "Foundation; either version 2 of the License, or (at your "
                   "option) any later version. "
                   "\n"
                   "Seqdiag GUI is distributed in the hope that it will be "
                   "useful, but WITHOUT ANY WARRANTY; without even the implied "
                   "warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR "
                   "PURPOSE.  See the GNU General Public License for more "
                   "details. You should have received a copy of the GNU "
                   "General Public License along with File Hunter; if not, "
                   "write to the Free Software Foundation, Inc., 59 Temple "
                   "Place, Suite 330, Boston, MA  02111-1307  USA")
        info = wx.AboutDialogInfo()
        info.SetName('Seqdiag GUI')
        info.SetVersion('0.1a1')
        info.SetDescription(desc)
        info.SetCopyright('(C) 2012 Luis Osa')
        info.SetWebSite('http://github.com/logc/seqdiag_gui')
        info.AddDeveloper('Luis Osa')
        info.AddDocWriter('Luis Osa')
        info.SetLicence(license)
        wx.AboutBox(info)

    def on_exit(self, event):
        """Exits the main window"""
        del event
        self.Close()  # Close the main window.

    def on_edit(self, event):
        """Evaluates the entered text at each edition"""
        del event
        diagram_tree = text2diagram(self.control.GetValue())
        if diagram_tree:
            self.status_bar.SetStatusText("")
            self.img.SetBackgroundColour(wx.NullColour)
            img = diagram2png(diagram_tree)
            stream = wx.InputStream(cStringIO.StringIO(img))
            png = wx.ImageFromStream(stream)
            self.img.SetBitmap(png.ConvertToBitmap())
        else:
            ## the colour is named 'tomato3' on
            ## http://web.njit.edu/~kevin/rgb.txt.html
            self.status_bar.SetStatusText(("Text edition does not evaluate to "
                                           "a valid seqdiagram"))
            self.img.SetBackgroundColour(wx.Colour(205, 79, 57))
            self.img.Refresh()

    def on_help(self, event):
        del event
        doc = DocWindow()
        doc.ShowModal()
        doc.Destroy()

    def on_save_button(self, event):
        """Select what to do when the user clicks on the 'Save' button"""
        if not self.already_saved:
            self.on_save_as(event)
        else:
            self.on_save(event)

    def on_save_as(self, event):
        """Saves the output graph to a file, whose filename must be provided by
        the user"""
        if self.ask_user_for_filename(defaultFile=self.imgfile, style=wx.SAVE,
                                      **self.default_file_dialog_options()):
            self.on_save(event)

    def on_save(self, event):
        """Saves the output graph to a file"""
        del event
        self.img.GetBitmap().ConvertToImage().SaveFile(
                os.path.join(self.dirname, self.filename), wx.BITMAP_TYPE_PNG)
        if not self.already_saved:
            self.already_saved = True

    def on_open(self, event):
        """Opens a text file to edit"""
        del event
        if self.ask_user_for_filename(style=wx.OPEN,
                **self.default_file_dialog_options()):
            textfile = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(textfile.read())
            textfile.close()

class HtmlWindow(wx.html.HtmlWindow):
    """HtmlWindow as seen in the WxPython wiki:
       http://wiki.wxpython.org/wxPython%20by%20Example"""

    def __init__(self, parent, id):
        wx.html.HtmlWindow.__init__(self,parent, id)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class DocWindow(wx.Dialog):
    """DocWindow is a dialog that holds documentation about this application"""
    def __init__(self):
        wx.Dialog.__init__(self, None, -1,
                "Seqdiag GUI documentation",
                style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                      wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, wx.ID_ANY)
        htmlText = open(HELP_PAGE).read()
        hwin.SetPage(htmlText)
