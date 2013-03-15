import wx


def build_menubar(mainwindow):
    """builds a menu bar for the main window"""
    file_menu = wx.Menu()
    for item_id, label, help_text, handler in \
        [(wx.ID_ABOUT, '&About', 'Information about this program',
            mainwindow.on_about),
         (wx.ID_OPEN, '&Open', 'Open a new file', mainwindow.on_open),
         (wx.ID_SAVE, '&Save', 'Save the current file', mainwindow.on_save),
         (wx.ID_SAVEAS, 'Save &As', 'Save the file under a different name',
            mainwindow.on_save_as),
         (None, None, None, None),
         (wx.ID_EXIT, 'E&xit', 'Terminate the program', mainwindow.on_exit)]:
        if item_id is None:
            file_menu.AppendSeparator()
        else:
            item = file_menu.Append(item_id, label, help_text)
            mainwindow.Bind(wx.EVT_MENU, handler, item)
    help_menu = wx.Menu()
    help_item = help_menu.Append(wx.ID_HELP, '&Documentation',
                                 'Help on this application')
    mainwindow.Bind(wx.EVT_MENU, mainwindow.on_help, help_item)
    menu_bar = wx.MenuBar()
    menu_bar.Append(file_menu, '&File')
    menu_bar.Append(help_menu, '&Help')
    return menu_bar
