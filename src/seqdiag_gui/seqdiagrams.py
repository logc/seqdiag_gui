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
