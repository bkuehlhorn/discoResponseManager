

import json
import os

import tkinter
import tkinter.ttk as ttk
from flatDict.flatDict import *
from discoResponseManager import logger
from xmltodict import parse, ParsingInterrupted
from functools import reduce

FLATKEYSDEPTH = collections.namedtuple('FLATKEYSDEPTH', 'items keys')
RESPONSE_ENTRY = collections.namedtuple('RESPONSE_ENTRY', 'success show response, allKeys type')
TABLE_ENTRY = collections.namedtuple('TABLE_ENTRY', 'parent text values tags')
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


class DiscoTree(ttk.Treeview):
    responses = []

    class PopupUpdateValue(ttk.Frame):
        """
        Pop up to enter value for selected field
        """
        def __init__(self, parent, title, body, row, column, value, response_file):
            """
            Creeate pop up to replace cell.

            :param parent:
            :param title:
            :param body:
            :param row:
            :param column:
            :param value:
            """
            ttk.Frame.__init__(self, parent)
            self.top = tkinter.Toplevel(parent)
            self.top.title(title)
            self.label = ttk.Label(self.top, text=body, justify=tkinter.LEFT)
            self.label.grid(row=1, column=1, sticky='E', padx=10, pady=10)
            self.e = ttk.Entry(self.top)
            self.e.grid(row=2, column=1, pady=10)
            self.e.focus_set()
            self.row = row
            self.column = column
            self.response_file = response_file
            self.button = ttk.Button(self.top, text=_("OK"), command=self.setValueButton)
            self.button.grid(row=3, column=1)

            self.button_cancel = ttk.Button(self.top, text=_("Cancel"), command=self.cancelButton)
            self.button_cancel.grid(row=3, column=2)

            logger.debug(f'popup: {(row, column, value)}')

        def setValueButton(self):
            logger.debug('ok button hit')
            self.value = self.e.get()
            logger.debug(f'values: {self.value}')
            self.top.destroy()
            values = self.master.item(self.row)['values']
            values[int(self.column[1:]) - 1] = self.value
            self.master.responses[self.response_file].response.addValue(self.row, self.value)
            self.master.item(self.row, values=values)
            self.master.responses[self.master.column(self.column)['id']].response[self.row] = self.value
            pass

        def cancelButton(self):
            logger.debug('cancel button hit')
            self.top.destroy()
            pass


    class PopupSaveFile(ttk.Frame):
        """
        Pop up to enter value for selected field
        """

        def __init__(self, parent, title, body, row, column, filename):
            """
            Creeate pop up to replace cell.

            :param parent:
            :param title:
            :param body:
            :param row:
            :param column:
            :param value:
            """
            ttk.Frame.__init__(self, parent)
            self.top = tkinter.Toplevel(parent)
            self.top.title(title)
            self.label = ttk.Label(self.top, text=body, justify=tkinter.LEFT)
            self.label.grid(row=1, column=1, sticky='E', padx=10, pady=10)
            # self.e = ttk.Entry(self.top)
            # self.e.grid(row=2, column=1, pady=10)
            # self.e.focus_set()
            self.button_save = ttk.Button(self.top, text=_("Save"), command=self.saveButton)
            self.button_save.grid(row=3, column=1, pady=5)
            self.row = row
            self.column = column
            self.filename = filename

            self.button_cancel = ttk.Button(self.top, text=_("Cancel"), command=self.cancelButton)
            self.button_cancel.grid(row=3, column=2, pady=5)

            logger.debug(f'popug: {(row, column, filename)}')

        def saveButton(self):
            "OK button feedback."
            logger.debug('save button hit')
            # self.value = self.e.get()
            logger.debug(f'values: {self.filename}')
            if self.master.responses[self.filename].type == 'json':
                fullFile = os.path.join(self.master.responseFolder, self.filename)
                fp = open(fullFile, 'w')
                js = json.dumps(self.master.responses[self.filename].response, indent=4)
                json.dump(self.master.responses[self.filename].response, fp, indent=4)
                fp.close()
            elif self.master.responses[self.filename].type == 'xml':
                # js = xml .dumps(self.master.responses[self.filename].response)
                pass
                # save string in file
            else:
                # add error details
                logger.warn(f'file is not saved: {self.filename}, {self.master.responses[self.filename].type}')
            self.top.destroy()
            self.master.set(self.master.rowid, self.master.columnid, self.filename)
            pass

        def cancelButton(self):
            "Concel button feedback."
            logger.debug('cancel button hit')
            self.top.destroy()
            pass

    def callback(self, event):
        rowid = self.identify_row(event.y)
        column = self.identify_column(event.x)
        selItems = self.selection()
        # col = int(column[1]) - 1
        if rowid == '':
            logger.debug('Click on header')
            if column == '#0':
                logger.debug('Cell data:', 'row heading: ', selItems)
            else:
                # logger.debug(f'Cell data: column heading: {self["column"][column]}')
                _description = _(f'promptd to edit or save response: {self["column"][int(column[1:])-1]}.')
                self.rowid = rowid
                self.columnid = column
                filename = self.column(int(column[1:])-1)['id']
                self.PopupSaveFile(self, f'Disco Response Manager - Save: ', _description, rowid, column, filename)
        else:
            if self.item(rowid)["values"][int(column[1:]) - 1] == 'None':
                logger.debug(f'Click on row: {rowid}')
                _description = _(f'Current {rowid}: Can not edit.')
                filename = self.column(int(column[1:]) - 1)['id']
                PopupDialog(self, f'Update {filename}:', _description)
            else:
                logger.debug(f'Click on row: {rowid}')
                _description = _(f'Current {rowid}: {self.item(rowid)["values"][int(column[1:]) - 1]}.')
                filename = self.column(int(column[1:]) - 1)['id']
                self.PopupUpdateValue(self, f'Update {filename}:', _description, rowid, column, selItems, filename)


    def __init__(self, parent, responseFolder):
        logger.debug(f'init: {responseFolder}')
        ttk.Treeview.__init__(self, parent)
        self.responseFolder = responseFolder
        # self.tag_configure('diff', background='aquamarine1')
        self.tag_configure('missing', background='aquamarine1') #, relief='raised')
        vsb = ttk.Scrollbar(parent, orient='vertical', command=self.yview)
        hsb = ttk.Scrollbar(parent, orient='horizontal', command=self.xview)
        self.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.grid(column=0, row=0, sticky='nsew', in_=parent)
        vsb.grid(column=1, row=0, sticky='ns', in_=parent)
        hsb.grid(column=0, row=1, sticky='ew', in_=parent)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        # self.bind('<Button-1>', callback)
        self.bind('<Double-Button-1>', self.callback)

        if self.responseFolder != '' and os.path.exists(self.responseFolder):
            responses = self.getResponses(self.responseFolder)
            self.renderTree(responses)


    def updateTree(self, responseFolder):
        logger.debug(f'update: {responseFolder}')
        self.responseFolder = responseFolder
        if self.responseFolder != '' and os.path.exists(self.responseFolder):
            responses = self.getResponses(self.responseFolder)
            self.renderTree(responses)


    def insertTree(self, flat_keys, responses):
        """

        return new_tree with row for each partial key from flatKeys
            parent, 'end', next_parent, None, text, tag_list, value_list

        Bug: Extra columns are added for dict with sub elements

        :param flat_keys: sorted list of full keys for all responses
        :param responses: list of RESPONSE_ENTRY
        :param table_entries: TABLE_ENTRY, parent text values tags
        :return:
        """
        table_entries = {}
        responses_keys = list(responses.keys())
        value = {'': {}}
        for response_file in responses.keys():
            value[''][response_file] = responses[response_file].response

        for flat_key in flat_keys:
            tags = collections.OrderedDict(list(map(lambda x: ('', None), responses.keys())))
            parent = ''
            flat_key_parts = flat_key.split(FlatDict.DELIMITER)
            flat_key_parts_list = [False] * len(flat_key_parts)
            logger.debug(f'flat key: {flat_key}')
            flat_key_parts_index = 0
            reset_index = False
            while flat_key_parts_index < len(flat_key_parts):
                flat_key_part = flat_key_parts[flat_key_parts_index]
                flat_key_part_done = True
                if parent == '':
                    next_parent = flat_key_part
                else:
                    next_parent = ':'.join([parent, str(flat_key_part)])
                if  isinstance(flat_key_part, str) and flat_key_part.isnumeric():
                    flat_key_part = int(flat_key_part)
                    flat_key_parts[flat_key_parts_index] = flat_key_part

                logger.debug(f'\tflat_key_part: {flat_key_part}')
                num_none_entries = 0
                for responses_keys_index in range(len(responses_keys)):
                    response_file = responses_keys[responses_keys_index]
                    logger.debug(f'\t\tprocess file: {response_file}')
                    if next_parent not in table_entries:
                        table_entries[next_parent] = TABLE_ENTRY(parent, flat_key_part, [], [None] * len(responses_keys))
                        value[next_parent] = {response_file: None}
                        table_entries[next_parent].tags[responses_keys_index] = None
                        logger.debug(f'\t\t\tAdding table row: {next_parent}')
                    if value[parent][response_file] is None:
                        table_entries[next_parent].values.append(None)
                        value[next_parent][response_file] = None
                        table_entries[next_parent].tags[responses_keys_index] = 'missing'
                        tags[next_parent] = 'missing'
                        logger.debug(f'\t\t\tcontinue missing element: {flat_key_part}')
                    else:
                        if isinstance(value[parent][response_file], dict):
                            if tags[parent] == 'missing' or flat_key_part not in value[parent][response_file]:
                                table_entries[next_parent].values.append(None)
                                value[next_parent][response_file] = None
                                tags[next_parent] = None
                                table_entries[next_parent].tags[responses_keys_index] = 'missing'
                                # num_none_entries += 1
                                logger.debug(f'\t\t\tcontinue missing dict: {flat_key_part}')
                            else:
                                if isinstance(value[parent][response_file][flat_key_part], (dict, list)):
                                    table_entries[next_parent].values.append(None)
                                    value[next_parent][response_file] = value[parent][response_file][flat_key_part]
                                    tags[next_parent] = None
                                    logger.debug(f'\t\t\tcontinue next dict/list: {flat_key_part}')
                                else:
                                    table_entries[next_parent].values.append(value[parent][response_file][flat_key_part])
                                    # value[next_parent][response_file] = value[parent][response_file][flat_key_part]
                                    # table_entries[next_parent].tags
                                    tags[next_parent] = None
                                    logger.debug(f'\t\t\tcontinue got a value: {value[parent][response_file][flat_key_part]}')
                                    flat_key_part_done = True
                        elif isinstance(value[parent][response_file], list):
                            if tags[parent] == 'missing' or flat_key_part >= len(value[parent][response_file]):
                                table_entries[next_parent].values.append(None)
                                value[next_parent][response_file] = None
                                table_entries[next_parent].tags[responses_keys_index] = 'missing'
                                tags[next_parent] = 'missing'
                                num_none_entries += 1
                                logger.debug(f'\t\t\tcontinue missing list: {flat_key_part}')
                            else:
                                flat_key_parts_list[flat_key_parts_index] = True
                                if isinstance(value[parent][response_file][flat_key_part], (dict, list)):
                                    table_entries[next_parent].values.append(None)
                                    value[next_parent][response_file] = value[parent][response_file][flat_key_part]
                                    tags[next_parent] = None
                                    logger.debug(f'\t\t\tcontinue next dict/list: {flat_key_part}')
                                else:
                                    table_entries[next_parent].values.append(value[parent][response_file][flat_key_part])
                                    # value
                                    tags[next_parent] = None
                                    logger.debug(f'\t\t\tcontinue got a value: {value[parent][response_file][flat_key_part]}')
                                    flat_key_part_done = flat_key_part >= (len(value[parent]) - 1)
                        else:
                            table_entries[next_parent].values.append(value[parent][response_file][flat_key_part])
                            # value
                            table_entries[next_parent].tags[responses_keys_index] = None
                            tags[next_parent] = None
                            logger.debug(f'\t\t\tcontinue value: {value[parent][response_file][flat_key_part]}')
                    # table_entries[next_parent].tags = tags[responses_keys_index]

                if flat_key_part_done:
                    logger.debug(f'Flat key done: {flat_key_parts} - {table_entries[next_parent].tags.count(None)}')
                    if table_entries[next_parent].tags.count('missing') == len(table_entries[next_parent].tags):
                    # if num_none_entries == len(responses.keys()):
                        # clean up extra None in last table entry
                        # table_entries.pop(parent)
                        table_entries.pop(next_parent)
                        flat_key_parts_index = len(flat_key_parts)
                        logger.debug(f'Remove extra list entries: {flat_key_parts_index}')
                    else:
                        logger.debug(f'Done with: {parent}/{next_parent}')
                        parent = next_parent
                        flat_key_parts_index += 1
                        if flat_key_parts_index >= len(flat_key_parts) and sum(flat_key_parts_list):
                            for index in range(1, len(flat_key_parts_list)+2):
                                if flat_key_parts_list[-index]:
                                    break
                            flat_key_parts_index = len(flat_key_parts_list) - index
                            for index in range(flat_key_parts_index+1, len(flat_key_parts)):
                                if isinstance(flat_key_parts[index], int):
                                    flat_key_parts[index] -= 1
                                    extra_entry_key = FlatDict.DELIMITER.join((map(lambda x: str(x), flat_key_parts[0:index])))
                                    table_entries.pop(extra_entry_key)
                                    flat_key_parts[index] = 0
                            flat_key_parts[flat_key_parts_index] += 1
                            parent = FlatDict.DELIMITER.join((map(lambda x: str(x), flat_key_parts[0:flat_key_parts_index])))
                            flat_key_parts_list[flat_key_parts_index] = False
                            logger.debug(f'New parent: {parent}')
                else:
                    flat_key_parts[flat_key_parts_index] = flat_key_part + 1
                    logger.debug(f'Try another List entry: {flat_key_parts}')
            pass
        return table_entries


    def getResponses(self, responseFolder):
        logger.debug(f'Get responses from {responseFolder}')
        responses = FlatDict()
        responseFileSet = set(os.listdir(responseFolder))
        successFile = 'success.json.erb'
        responseFileSet.discard(successFile)
        responseFiles = [successFile] + sorted(list(responseFileSet))  #[0:2]
        errorFiles = []

        for filename in responseFiles:
            logger.debug(f'\tfilename: {filename}')
            jsonInput = open(os.path.join(responseFolder, filename), 'r').read()
            if jsonInput.startswith('<?xml'):
                errorFiles.append(f'{filename}, reason:xml is not support, yet')
            else:
                try:
                    response = FlatDict(json.loads(jsonInput))
                    responses[filename] = RESPONSE_ENTRY(response['status']=='SUCCESS', response['status'].upper()=='SUCCESS', response, response.getKeys(), 'json')
                except (ValueError, json.JSONDecodeError) as e:
                    logger.info(f'json fails: filename:{filename}, reason:{e}')
                    errorFiles.append(f'{filename}, reason:{e}')
                except RuntimeError as e:
                    logger.info(f'RuntimeError: filename:{filename}, reason:{e}')
                    errorFiles.append(f'{filename}, reason:{e}')
        if len(errorFiles) > 0:
            description = f'Folder: {responseFolder} contains unsupported files:'
            for filename in errorFiles:
                description += f'\n\t{filename}'
            PopupDialog(self, 'Error Disco Response Manager',
                        description)

            logger.debug(f'problem with file {filename}')
        return responses

    def tag_callback(self, event):
        rowid = self.identify_row(event.y)
        column = self.identify_column(event.x)
        selItems = self.selection()
        # col = int(column[1]) - 1
        logger.debug(f'Click on tag: {rowid}')
        if int(column[1:]) == 0:
            logger.debug(f'index is row label: {column}')
            filename = 'Row Heading'
            return
        else:
            filename = self.column(int(column[1:]) - 1)['id']
        if self.item(rowid)["values"][int(column[1:]) - 1] == 'None':
            _description = _(f'Current {rowid}: {self.item(rowid)["values"][int(column[1:]) - 1]}.\nCan not edit field')
            PopupDialog(self, f'Tag {filename}:', _description)
        else:
            _description = _(f'Current {rowid}: {self.item(rowid)["values"][int(column[1:]) - 1]}.')
            self.PopupUpdateValue(self, f'Tag {filename}:', _description, rowid, column, selItems)

    def renderTree(self, all_responses):
        """
        Use

        create table for self:
        walk each response.response[]... to get value for column list

        :param self:
        :param responses:
        :return:
        """
        logger.debug(f'all_responses: {all_responses}')
        responses = dict(filter(lambda x: x[1].show, all_responses.items()))
        # responses = dict(list(filter(lambda x: x[1].show, all_responses.items()))[0:2])
        self.responses = responses
        def heading(column):
            logger.debug(f"click! {column}")

        responses['success.json.erb'] = all_responses['success.json.erb']
        successResponse = list(responses.keys())[0]
        columns = tuple(responses.keys())
        self["columns"] = columns
        # self["displaycolumns"] = columns
        # self.column(successResponse, width=200)
        for title in columns:
            self.heading(title, text=title)

        all_keys = set()
        for response in responses:
            all_keys = all_keys.union(responses[response].allKeys)

        all_keys = sorted(all_keys)
        tree_list = self.insertTree(all_keys, responses)
        pass
        # self.tag_bind('missing', '<1>', callback=self.tag_callback)
        for (iid, values) in tree_list.items():
            logger.debug(f'add: {iid}, {values}')
            try:
                self.insert(values.parent,
                            'end',
                            iid,
                            text=values.text,
                            tags=values.tags,
                            values=values.values)
            except tkinter.TclError as e:
                pass
