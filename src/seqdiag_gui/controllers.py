# Copyright (C) 2013 Luis Osa
#
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
File:
    controllers.py
Author:
    Luis Osa <logc>
Description:
    This module holds all Controllers. Controllers mediate the effects of user
    actions on the Models.
"""
import os.path

import wx

import handlers
from windows import MainWindow, DocWindow


class MainController(object):
    """Represents the controller for Main"""

    def __init__(self, app):
        self.app = app
        self.main_window = MainWindow()
        self.main_window.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        self.main_window.eval_button.Bind(wx.EVT_BUTTON, self.on_edit)
        self.already_saved = False
        self.imgfile = 'simple.png'
        self.filename = 'simple.diag'
        self.dirname = '.'
        self.main_window.SetTitle('Editing {0}'.format(self.filename))
        self.main_window.SetMenuBar(self.build_menubar())
        self.main_window.status_bar = self.main_window.CreateStatusBar()
        self.main_window.Show()

    def build_menubar(self):
        """builds a menu bar for the main window"""
        file_menu = wx.Menu()
        for item_id, label, help_text, handler in \
                [(wx.ID_ABOUT, '&About', 'Information about this program',
                    self.on_about),
                 (wx.ID_OPEN, '&Open', 'Open a new file', self.on_open),
                 (wx.ID_SAVE, '&Save', 'Save the current file', self.on_save),
                 (wx.ID_SAVEAS, 'Save &As',
                     'Save the file under a different name', self.on_save_as),
                 (None, None, None, None),
                 (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.on_exit)]:
            if item_id is None:
                file_menu.AppendSeparator()
            else:
                item = file_menu.Append(item_id, label, help_text)
                self.main_window.Bind(wx.EVT_MENU, handler, item)
        help_menu = wx.Menu()
        help_item = help_menu.Append(wx.ID_HELP, '&Documentation',
                                     'Help on this application')
        self.main_window.Bind(wx.EVT_MENU, self.on_help, help_item)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(help_menu, '&Help')
        return menu_bar

    def on_about(self, event):
        """Handles the event of clicking on the 'About' menu option"""
        event.Skip()
        wx.AboutBox(handlers.build_infobox())

    def on_exit(self, event):
        """Exits the main window"""
        event.Skip()
        self.main_window.Close()

    def on_edit(self, event):
        """Evaluates the entered text at each edition"""
        event.Skip()
        handlers.edit(self.main_window)

    def on_help(self, event):
        event.Skip()
        doc = DocWindow()
        doc.ShowModal()
        doc.Destroy()

    def on_save_as(self, event):
        """Saves the output graph to a file, whose filename must be provided by
        the user"""
        if self.ask_user_for_filename(defaultFile=self.imgfile, style=wx.SAVE,
                                      **self.default_file_dialog_options()):
            self.on_save(event)

    def on_save(self, event):
        """Saves the output graph to a file"""
        event.Skip()
        if not self.already_saved:
            self.on_save_as(event)
        else:
            self.main_window.img.GetBitmap().ConvertToImage().SaveFile(
                os.path.join(self.dirname, self.filename), wx.BITMAP_TYPE_PNG)
            self.already_saved = True

    def on_open(self, event):
        """Opens a text file to edit"""
        event.Skip()
        if self.ask_user_for_filename(style=wx.OPEN,
                                      **self.default_file_dialog_options()):
            textfile = open(os.path.join(self.dirname, self.filename), 'r')
            self.main_window.control.SetValue(textfile.read())
            textfile.close()

    def ask_user_for_filename(self, **dialogOptions):
        """Returns the success of asking the user, through a wx standard
        dialog, for a new filename to edit"""
        dialog = wx.FileDialog(self.main_window, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            filename_provided_by_user = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.set_title()  # Update the window title with the new filename
        else:
            filename_provided_by_user = False
        dialog.Destroy()
        return filename_provided_by_user

    def default_file_dialog_options(self):
        """Returns a dictionary with file dialog options that can be
        used in both the save file dialog as well as in the open file
        dialog. """
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.*')
