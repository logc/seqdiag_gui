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

from wx import AboutDialogInfo, Colour, InputStream, ImageFromStream, NullColour

from seqdiagrams import text2diagram, diagram2png

LICENSE = """

Seqdiag GUI is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

Seqdiag GUI is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details. You
should have received a copy of the GNU General Public License along with File
Hunter; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
Suite 330, Boston, MA  02111-1307 USA")

"""

def build_infobox():
    """builds an info box to show help"""
    desc = ("Seqdiag GUI is a a graphic user interface to Takeshi Komiya's "
            "simple sequence diagram package, called seqdiag")
    license = LICENSE
    info = AboutDialogInfo()
    info.SetName('Seqdiag GUI')
    info.SetVersion('0.1a1')
    info.SetDescription(desc)
    info.SetCopyright('(C) 2013 Luis Osa')
    info.SetWebSite('http://github.com/logc/seqdiag_gui')
    info.AddDeveloper('Luis Osa')
    info.AddDocWriter('Luis Osa')
    info.SetLicence(license)
    return info

def edit(mainwindow):
    """handles an edition in the text control by updating the diagram"""
    diagram_tree = text2diagram(mainwindow.control.GetValue())
    if diagram_tree:
        mainwindow.status_bar.SetStatusText("")
        mainwindow.img.SetBackgroundColour(NullColour)
        img = diagram2png(diagram_tree)
        stream = InputStream(cStringIO.StringIO(img))
        png = ImageFromStream(stream)
        mainwindow.img.SetBitmap(png.ConvertToBitmap())
    else:
        ## the colour is named 'tomato3' on
        ## http://web.njit.edu/~kevin/rgb.txt.html
        mainwindow.status_bar.SetStatusText(("Text edition does not evaluate to "
                                       "a valid seqdiagram"))
        mainwindow.img.SetBackgroundColour(Colour(205, 79, 57))
        mainwindow.img.Refresh()
