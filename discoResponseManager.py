"""
discoResponseManager
-----------------

GUI to manage emdpoint responses for Disco
"""

import argparse
import collections
import datetime
from discoResponses.discoResponses import *
from flatDict.flatDict import *
import gettext
import logging
import sys
import time
import tkinter
import tkinter.filedialog as fd
from tkinter import messagebox as msg
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
import json
import os
import queue
# import xmltodict


logger = logging.getLogger(__name__)

# All translations provided for illustrative purposes only.
# english
_ = lambda s: s


class PopupDialog(ttk.Frame):
    "Sample popup dialog implemented to provide feedback."

    def __init__(self, parent, title, body):
        ttk.Frame.__init__(self, parent)
        self.top = tkinter.Toplevel(parent)
        _label = ttk.Label(self.top, text=body, justify=tkinter.LEFT)
        _label.pack(padx=10, pady=10)
        _button = ttk.Button(self.top, text=_("OK"), command=self.ok_button)
        _button.pack(pady=5)
        self.top.title(title)

    def ok_button(self):
        "OK button feedback."

        self.top.destroy()


class NavigationBar(ttk.Frame):
    "Sample navigation pane provided by cookiecutter switch."

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.config(border=1, relief=tkinter.GROOVE)

        self.scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=1)

        self.listbox = tkinter.Listbox(self, bg='white')
        self.listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        for i in range(1, 100):
            self.listbox.insert(tkinter.END, _('Navigation ') + str(i))
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.bind_all('<<ListboxSelect>>', self.onselect)
        self.pack()

    def onselect(self, event):
        """Sample function provided to show how navigation commands may be \
        received."""

        widget = event.widget
        _index = int(widget.curselection()[0])
        _value = widget.get(_index)
        logger.debug(_('List item'), ' %d / %s' % (_index, _value))


class StatusBar(ttk.Frame):
    "Sample status bar provided by cookiecutter switch."
    _status_bars = 4

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.labels = []
        self.config(border=1, relief=tkinter.GROOVE)
        for i in range(self._status_bars):
            _label_text = _('Unset status ') + str(i + 1)
            self.labels.append(ttk.Label(self, text=_label_text))
            self.labels[i].config(relief=tkinter.GROOVE)
            self.labels[i].pack(side=tkinter.LEFT, fill=tkinter.X)
        self.pack()

    def set_text(self, status_index, new_text):
        self.labels[status_index].config(text=new_text)


class ToolBar(ttk.Frame):
    "Sample toolbar provided by cookiecutter switch."

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.buttons = []
        self.config(border=1, relief=tkinter.GROOVE)
        for i in range(1, 5):
            _button_text = _('Tool ') + str(i)
            self.buttons.append(ttk.Button(self, text=_button_text,
                                           command=lambda i=i: self.run_tool(i)))
            self.buttons[i - 1].pack(side=tkinter.LEFT, fill=tkinter.X)
        self.pack()

    def run_tool(self, number):
        "Sample function provided to show how a toolbar command may be used."

        logger.debug(_('Toolbar button'), number, _('pressed'))


class MainFrame(ttk.Frame):
    "Main area of user interface content."

    past_time = datetime.datetime.now()
    _advertisement = 'Cookiecutter: Open-Source Project Templates'
    _product = _('Template') + ': Disco Response Manager'
    _boilerplate = _advertisement + '\n\n' + _product + '\n\n'

    def __init__(self, parent, responseFolder):
        ttk.Frame.__init__(self, parent)
        # self.display = ttk.Label(parent, anchor=tkinter.CENTER,
        #                          foreground='green', background='black')
        # self.display.pack(fill=tkinter.BOTH, expand=1)
        # self.tick()
        self.tree = DiscoTree(self, parent.responseFolder)
        pass

    def tick(self):
        "Invoked automatically to update a clock displayed in the GUI."

        this_time = datetime.datetime.now()
        if this_time != self.past_time:
            self.past_time = this_time
            _timestamp = this_time.strftime('%Y-%m-%d %H:%M:%S')
            self.display.config(text=self._boilerplate + _timestamp)
        self.display.after(100, self.tick)


class MenuBar(tkinter.Menu):
    "Menu bar appearing with expected components."

    def __init__(self, parent):
        tkinter.Menu.__init__(self, parent)
        self.parent = parent

        logger.debug('Create Menu')
        filemenu = tkinter.Menu(self, tearoff=False)
        # filemenu.add_command(label=_('New'), command=self.new_dialog)
        filemenu.add_command(label=_('Open'), command=self.open_dialog)
        filemenu.add_separator()
        filemenu.add_command(label=_('Exit'), underline=1,
                             command=self.quit)

        helpmenu = tkinter.Menu(self, tearoff=False)
        helpmenu.add_command(label=_('Help'), command=lambda:
        self.help_dialog(None), accelerator="F1")
        helpmenu.add_command(label=_('About'), command=self.about_dialog)
        self.bind_all('<F1>', self.help_dialog)

        self.add_cascade(label=_('File'), underline=0, menu=filemenu)
        self.add_cascade(label=_('Help'), underline=0, menu=helpmenu)

    def quit(self):
        "Ends toplevel execution."
        logger.debug('App stopped')

        sys.exit(0)

    def help_dialog(self, event):
        "Dialog cataloging results achievable, and provided means available."

        description = _(f'Using: {self.parent.responseFolder}.')
        PopupDialog(self, 'Disco Response Manager', description)

    def about_dialog(self):
        "Dialog concerning information about entities responsible for program."

        _description = 'GUI to manage emdpoint responses for Disco'
        if _description == '':
            _description = _('No description available')
        _description += '\n'
        _description += '\n' + _('Author') + ': Bernard Kuehlhorn'
        _description += '\n' + _('Email') + ': bkuehlhorn@acm.org'
        _description += '\n' + _('Version') + ': 0.0.1'
        _description += '\n' + _('GitHub Package') + \
                        ': discoResponseManager'
        PopupDialog(self, _('About') + ' Disco Response Manager',
                    _description)

    def new_dialog(self):
        "Non-functional dialog indicating successful navigation."

        PopupDialog(self, _('New button pressed'), _('Not yet implemented'))

    def open_dialog(self):
        "Standard askopenfilename() invocation and result handling."

        responseFolder = fd.askdirectory(title="Open directory",
                                         initialdir=".")
        if responseFolder:
            logger.debug(responseFolder)
            requiredResponseFile = 'success.json.erb'
            if os.path.exists(os.path.join(responseFolder, requiredResponseFile)):
                # responses = self.master.mainframe.tree.getResponses(responseFolder)
                # self.master.mainframe.tree.renderTree(responses)
                self.master.wm_title(f'Disco Response Manager: {responseFolder.split("/")[-1]}')
                r0 = self.master.mainframe.tree.get_children()
                self.master.mainframe.tree.delete(*r0)
                self.master.mainframe.tree.updateTree(responseFolder)
                # self.master.mainframe.tree.pack(side='right', fill='y')
                pass
            else:
                msg.showwarning('Incomplete Response Folder',
                                f'Folder does not contain {requiredResponseFile}\nChoose a different Response Folder.')

    def exitResponse(self):
        exit()

    def callback(self, event):
        rowid = self.identify_row(event.y)
        column = self.identify_column(event.x)
        selItems = self.selection()
        if selItems:
            selItem = selItems[0]
            text = self.item(selItem, 'values')
            cell = int(column[1]) - 1
            if rowid == '':
                logger.debug('Click on header')
            else:
                logger.debug(f'Click on row: {rowid}')
            textPrint = set(text)
            textPrint.discard('None')
            logger.debug('Row data: {textPrint}')
            logger.debug('Clicked on Cell: {cell}')
            if cell == -1:
                logger.debug('Cell data:', 'row heading')
            else:
                if len(text) > 0:
                    logger.debug(f'Cell data: {text[cell]}', )
                else:
                    logger.debug('Cell data: None')


class Application(tkinter.Tk):
    "Create top-level Tkinter widget containing all other widgets."

    def __init__(self, args):
        if args.verbouse is not None and int(args.verbouse) > 0:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        logger.debug('App started')
        # if folder preset prepare to render responses
        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.wm_title(f'Disco Response Manager: {args.responseFolder.split("/")[-1]}')
        self.wm_geometry('640x480')

        # Status bar selection == 'y'
        self.statusbar = StatusBar(self)
        self.statusbar.pack(side='bottom', fill='x')
        self.bind_all('<Enter>',
                      lambda e: self.statusbar.set_text(0, 'Mouse: 1'))
        self.bind_all('<Leave>',
                      lambda e: self.statusbar.set_text(0, 'Mouse: 0'))
        self.bind_all('<Button-1>',
                      lambda e: self.statusbar.set_text(1, 'Clicked at x = ' + str(e.x) + ' y = ' + str(e.y)))
        self.start_time = datetime.datetime.now()
        self.uptime()

        # Navigation selection == 'y'
        # self.navigationbar = NavigationBar(self)
        # self.navigationbar.pack(side='left', fill='y')

        # Tool bar selection == 'y'
        self.toolbar = ToolBar(self)
        self.toolbar.pack(side='top', fill='x')

        self.responseFolder = args.responseFolder
        self.mainframe = MainFrame(self, self.responseFolder)
        self.mainframe.pack(side='right', fill='y')

    # Status bar selection == 'y'
    def uptime(self):
        _upseconds = str(int(round((datetime.datetime.now() - self.start_time).total_seconds())))
        self.statusbar.set_text(2, _('Uptime') + ': ' + _upseconds)
        self.after(1000, self.uptime)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('responseFolder', default='', nargs='?',
                   help='Input response folder')
parser.add_argument('-o', '--output', help='Output response folder')
parser.add_argument('-v', '--verbouse', dest='verbouse')
# parser.add_argument('-v', '--verbouse', dest='verbouse', action='store',
#                     const=4, default=0,
#                    help='Level of detail: 0-INFO, 1-DEBUG')

if __name__ == '__main__':
    args = parser.parse_args()
    APPLICATION_GUI = Application(args)
    APPLICATION_GUI.mainloop()
