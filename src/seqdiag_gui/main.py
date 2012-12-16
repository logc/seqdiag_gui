"""
Module main

main is the entry point of this application.
"""
import wx
import os.path
import cStringIO

from seqdiag import parser
from seqdiag.drawer import DiagramDraw
from seqdiag.builder import ScreenNodeBuilder

FORMAT = 'PNG'
ANTIALIAS = False
FONTPATH = None

def text2diagram(text):
    """Converts a text to an abstract diagram, which is not yet a
    representable image"""
    try:
        tree = parser.parse_string(text)
    except parser.ParseException:
        return None
    return ScreenNodeBuilder.build(tree)

def diagram2png(diagram):
    """Converts an abstract diagram into a representable image"""
    drawer = DiagramDraw(FORMAT, diagram,
                         font=FONTPATH,
                         antialias=ANTIALIAS,
                         transparency=True)
    drawer.draw()
    img = drawer.save()
    return img

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
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File') # Add the file_menu to the MenuBar
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
        dialog = wx.MessageDialog(self, 'A sample editor\n'
            'in wxPython', 'About Sample Editor', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

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

def run():
    """Application entry point"""
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
