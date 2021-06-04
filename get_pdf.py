"""
@created: 2018-08-19 18:00:00
@author: (c) 2018 Jorj X. McKie
Display a PyMuPDF Document using Tkinter
-------------------------------------------------------------------------------
Dependencies:
-------------
PyMuPDF, PySimpleGUI > v2.9.0, Tkinter with Tk v8.6+, Python 3
License:
--------
GNU GPL V3+
Description
------------
Read filename from command line and start display with page 1.
Pages can be directly jumped to, or buttons for paging can be used.
For experimental / demonstration purposes, we have included options to zoom
into the four page quadrants (top-left, bottom-right, etc.).
We also interpret keyboard events to support paging by PageDown / PageUp
keys as if the resp. buttons were clicked. Similarly, we do not include
a 'Quit' button. Instead, the ESCAPE key can be used, or cancelling the window.
To improve paging performance, we are not directly creating pixmaps from
pages, but instead from the fitz.DisplayList of the page. A display list
will be stored in a list and looked up by page number. This way, zooming
pixmaps and page re-visits will re-use a once-created display list.
"""
import sys
import fitz
import PySimpleGUI as sg
from sys import exit


def get_page(pno,fname):
    zoom = 0
    doc = fitz.open(fname)
    page_count = len(doc)

# storage for page display lists
    dlist_tab = [None] * page_count

    title = "PyMuPDF display of '%s', pages: %i" % (fname, page_count)



    """Return a PNG image for a document page number. If zoom is other than 0, one of the 4 page quadrants are zoomed-in instead and the corresponding clip returned.
    """
    dlist = dlist_tab[pno]  # get display list
    if not dlist:  # create if not yet there
        dlist_tab[pno] = doc[pno].getDisplayList()
        dlist = dlist_tab[pno]
    r = dlist.rect  # page rectangle
    mp = r.tl + (r.br - r.tl) * 0.5  # rect middle point
    mt = r.tl + (r.tr - r.tl) * 0.5  # middle of top edge
    ml = r.tl + (r.bl - r.tl) * 0.5  # middle of left edge
    mr = r.tr + (r.br - r.tr) * 0.5  # middle of right egde
    mb = r.bl + (r.br - r.bl) * 0.5  # middle of bottom edge
    mat = fitz.Matrix(2, 2)  # zoom matrix
    if zoom == 1:  # top-left quadrant
        clip = fitz.Rect(r.tl, mp)
    elif zoom == 4:  # bot-right quadrant
        clip = fitz.Rect(mp, r.br)
    elif zoom == 2:  # top-right
        clip = fitz.Rect(mt, mr)
    elif zoom == 3:  # bot-left
        clip = fitz.Rect(ml, mb)
    if zoom == 0:  # total page
        pix = dlist.getPixmap(alpha=False)
    else:
        pix = dlist.getPixmap(alpha=False, matrix=mat, clip=clip)
    return pix.getPNGData()  # return the PNG image

    