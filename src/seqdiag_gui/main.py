import wx
import seqdiag
import os.path

class SeqdiagImage():

    def text2diagram(self, text):
        tree = parser.parse_string(text)
        return ScreenNodeBuilder.build(tree)

    def diagram2png(self, diagram):
        pass

class MainWindow(wx.Frame):
    def __init__(self, filename='simple.diag', imgfile='simple.png'):
        super(MainWindow, self).__init__(None, size=wx.DefaultSize) #(400,200))
        self.filename = filename
        self.imgfile = imgfile
        self.dirname = '.'
        p = wx.Panel(self, -1)
        self.CreateInteriorWindowComponents(p)
        self.CreateExteriorWindowComponents()
        self.sizer = self.__arrange_boxes()
        p.SetSizer(self.sizer)
        self.sizer.Fit(p)
        self.Fit()

    def __arrange_boxes(self):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.img, 0, wx.EXPAND)
        box.Add(self.control, 0, wx.EXPAND)
        return box

    def CreateInteriorWindowComponents(self, panel):
        ''' Create interior window components, i.e. everythin except status
        and menu bars.'''
        self.control = wx.TextCtrl(panel, -1, open(self.filename, 'r').read(),
                                   style=wx.TE_MULTILINE)
        png = wx.Image(self.imgfile, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.img = wx.StaticBitmap(panel, -1, png,
                                   (png.GetWidth(), png.GetHeight()))

    def CreateExteriorWindowComponents(self):
        ''' Create exterior window components, such as menu and status bar.'''
        self.CreateMenu()
        self.SetTitle()

    def CreateMenu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [(wx.ID_ABOUT, '&About', 'Information about this program',
                self.OnAbout),
             (wx.ID_OPEN, '&Open', 'Open a new file', self.OnOpen),
             (wx.ID_SAVE, '&Save', 'Save the current file', self.OnSave),
             (wx.ID_SAVEAS, 'Save &As', 'Save the file under a different name',
                self.OnSaveAs),
             (None, None, None, None),
             (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File') # Add the fileMenu to the MenuBar
        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    def SetTitle(self):
        super(MainWindow, self).SetTitle('Editor %s'%self.filename)

    # Helper methods:

    def defaultFileDialogOptions(self):
        ''' Return a dictionary with file dialog options that can be
            used in both the save file dialog as well as in the open
            file dialog. '''
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.*')

    def askUserForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.SetTitle() # Update the window title with the new filename
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename

    # Event handlers:

    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, 'A sample editor\n'
            'in wxPython', 'About Sample Editor', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def OnSave(self, event):
        textfile = open(os.path.join(self.dirname, self.filename), 'w')
        textfile.write(self.control.GetValue())
        textfile.close()

    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.OPEN,
                                   **self.defaultFileDialogOptions()):
            textfile = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(textfile.read())
            textfile.close()

    def OnSaveAs(self, event):
        if self.askUserForFilename(defaultFile=self.filename, style=wx.SAVE,
                                   **self.defaultFileDialogOptions()):
            self.OnSave(event)

def run():
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()

