

import json
import os

import tkinter
import tkinter.ttk as ttk
from flatDict.flatDict import *
from discoResponseManager import logger
from xmltodict import parse, ParsingInterrupted

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
        def __init__(self, parent, title, body, row, column, value):
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
            self.button = ttk.Button(self.top, text=_("OK"), command=self.setValueButton)
            self.button.grid(row=3, column=1)

            self.button_cancel = ttk.Button(self.top, text=_("Cancel"), command=self.cancelButton)
            self.button_cancel.grid(row=3, column=2)

            logger.debug(f'popup: {(row, column, value)}')

        def setValueButton(self):
            "OK button feedback."
            logger.debug('ok button hit')
            self.value = self.e.get()
            logger.debug(f'values: {self.value}')
            self.top.destroy()
            values = self.master.item(self.row)['values']
            values[int(self.column[1:]) - 1] = self.value
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
            self.e = ttk.Entry(self.top)
            self.e.grid(row=2, column=1, pady=10)
            self.e.focus_set()
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
                _description = _(f'promptd to edit or save response: {self["column"][int(column[1:])]}.')
                self.rowid = rowid
                self.columnid = column
                filename = self.column(int(column[1:])-1)['id']
                self.PopupSaveFile(self, f'Disco Response Manager - Save: ', _description, rowid, column, filename)
        else:
            logger.debug(f'Click on row: {rowid}')
            _description = _(f'Current {rowid}: {self.item(rowid)["values"][int(column[1:]) - 1]}.')
            filename = self.column(int(column[1:]) - 1)['id']
            self.PopupUpdateValue(self, f'Update {filename}:', _description, rowid, column, selItems)

        # if selItems:
        #     # selItem = selItems[0]
        #     text = self.set(rowid, column)
        #     # textPrint = set(text)
        #     # textPrint.discard('None')
        #     logger.debug(f'Row data: {text}')
        #     if column == '#0':
        #         logger.debug('no cell reference')
        #     else:
        #         logger.debug(f'Clicked on Collumn: {column}')
        #         logger.debug(f'Column data: {text}')
        # else:
        #     logger.debug(f'Clicked on Column: {column}')
        #     logger.debug('Column heading')


    def __init__(self, parent, responseFolder):
        logger.debug(f'init: {responseFolder}')
        ttk.Treeview.__init__(self, parent)
        self.responseFolder = responseFolder
        self.tag_configure('diff', background='aquamarine1')
        self.tag_configure('missing', background='aquamarine1')
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


    def insertTreeO(self, flatKeys, responses):
        """
        Use flatKeys to find values in responses
        Add each part of flatKey to tree
        when part is not in response:
          mark response column for update
          add key to column menu selection

        goal: create tkTree from flatKeys
            each flatKey has keys to leaf
            split flatKey into flatKeys
            removeKeys = true
            stackIndex = 0
            for response in responses:
                for key in flatKeys:
                    (stack of keys)
                    (stack of nodes | value)
                    if removeKeys:
                        if stack of keys[stackIndex] == key:
                            stackIndex += 1
                        else:
                            del extra stack of keys
                            del extra stack of keys
                            removeKeys = false
                    else
                        push key on stack of keys
                        push top of stack of values (key) on values
                        insert into tree: item, 'end', key, text=key, values=value[responseToken].items, tags=tagL
                            item: keys up to last entry
                            'end': end of tree - may be wrong when building depth first
                            key: current node for tree
                            text: display for current node
                            values: tuple of values from response files for current flatKey
                            tags: tags defined in tree to manage css


        :param flatKeys:
        :param responses:
        :param tree:
        :return:
        """
        value = collections.OrderedDict(list(map(lambda x: (x, FLATKEYSDEPTH([], '', [], [])), responses.keys())))
        newTree = collections.OrderedDict(list(map(lambda x: (x, []), responses.keys())))

        for flatKey in flatKeys:
            flatKeyParts = flatKey.split(FlatDict.delimiter)
            logger.debug(f'flatKeyParts: {flatKeyParts}')
            for responseToken in responses:
                tagL = ''
                stackI = 0
                removeKeys = True
                for newPart in flatKeyParts:
                    logger.debug(f'\tnewPart: {newPart}, {removeKeys}')
                    if removeKeys:
                        logger.debug(f'\t\tstackI: {stackI}')
                        if stackI < len(value[responseToken].keys) and value[responseToken].keys[stackI] == newPart:
                            stackI += 1
                        else:
                            del value[responseToken].keys[stackI:]
                            del value[responseToken].items[stackI:]
                            removeKeys = False
                    if not removeKeys: # not else. need to process newPart not in value[responseToken].keys
                        if newPart.isnumeric():
                            newPart = int(newPart)
                        logger.debug(f'\t\tresponseToken: {responseToken}: {newPart}')
                        if len(value[responseToken].items) == 0 and newPart in responses[responseToken].response:
                            value[responseToken].items.append(responses[responseToken].response[newPart])
                        else:
                            try:
                                if tagL == '' and (len(value[responseToken].items) and newPart in value[responseToken].items[-1]):
                                    logger.debug(f'\t\t\tvalue: {value[responseToken].items[-1]}')
                                    value[responseToken].items.append(value[responseToken].items[-1][newPart])
                                else:
                                    tagL = 'missing'
                            except RuntimeError as e:
                                pass
                        item = ':'.join(value[responseToken].keys)
                        value[responseToken].keys.append(newPart if isinstance(newPart, str) else str(newPart))
                        if len(value[responseToken].items) > 0:
                            if isinstance(newPart, int):
                                pass
                                # newPart = f'{item}:{newPart}'
                            if isinstance(value[responseToken].items[-1], (dict, list)):
                                logger.debug(f'\t\t\tnewTree: {newPart}, None')
                                newTree[responseToken].append((item, 'end', newPart, newPart, None, tagL))
                            else:
                                logger.debug(f'\t\t\tnewTree: {newPart}, {value[responseToken].items[-1]}')
                                newTree[responseToken].append((item, 'end', newPart, newPart, (value[responseToken].items[-1]), tagL))

            pass
        for key, response in newTree.items():
            newTree[key] = sorted(response, key=lambda newNode: newNode[0])
        return newTree

    def insertTree(self, flat_keys, responses):
        """
        value = collections.OrderedDict(list(map(lambda x: (x, FLATKEYSDEPTH([], '', [], [])), responses.keys())))
        newTree = collections.OrderedDict(list(map(lambda x: (x, []), responses.keys())))
                            newTree[responseToken].append((item, 'end', newPart, newPart, (value[responseToken].items[-1]), tagL))

        return new_tree with row for each partial key from flatKeys
            parent, 'end', next_parent, None, text, tag_list, value_list

        initial: parent = '', next_parent = '', text = next_flat_entry, tag_list = [], value_list = []
        for flat_key in flat_keys:
            tags = None
            flat_key_parts = flat_key.split(FlatDict.DELIMITER)
            for flat_key_part in flat_key_parts:
                next_parent = FlatDict.DELIMTER.join(parent, flat_key_part)
                for response_file in responses.keys():
                    if parent == '':
                        speclial setup
                    else:
                        normal setup



        :param flatKeys:
        :param responses: list of RESPONSE_ENTRY
        :param tree:
        :return:

FLATKEYSDEPTH = collections.namedtuple('FLATKEYSDEPTH', 'items keys')
RESPONSE_ENTRY = collections.namedtuple('RESPONSE_ENTRY', 'success show response, allKeys type')
TABLE_ENTRY = collections.namedtuple('TABLE_ENTRY', 'iid text keys items')

        """
        newTree = collections.OrderedDict(list(map(lambda x: (x, []), responses.keys())))
        # table_entries = [parent text values tags]
        table_entries = {}

        for flat_key in flat_keys:
            tag = None
            value = collections.OrderedDict(list(map(lambda x: (x, [responses[x].response]), responses.keys())))
            tags = collections.OrderedDict(list(map(lambda x: (x, [None]), responses.keys())))
            parent = ''
            flat_key_parts = flat_key.split(':')
            # flat_key_parts = flat_key.split(FlatDict.DELIMITER)
            for flat_key_part in flat_key_parts:
                if parent == '':
                    next_parent = flat_key_part
                else:
                    next_parent = ':'.join([parent, flat_key_part])
                if flat_key_part.isnumeric():
                    flat_key_part = int(flat_key_part)

                for response_file in responses.keys():
                    if next_parent not in table_entries:
                        table_entries[next_parent] = TABLE_ENTRY(parent, flat_key_part, [], [])
                    if tags[response_file][-1] == 'missing' or flat_key_part not in value[response_file][-1]:
                        tag = 'missing'
                        value[response_file].append(None)
                        table_entries[next_parent].values.append(None)
                    else:
                        if isinstance(value[response_file][-1][flat_key_part], (dict, list)):
                            value[response_file].append(value[response_file][-1][flat_key_part])
                            table_entries[next_parent].values.append(None)
                        else:
                            table_entries[next_parent].values.append(value[response_file][-1][flat_key_part])
                    table_entries[next_parent].tags.append(tags[response_file][-1])
                    tags[response_file].append(tag)

                parent = next_parent
            pass
        # for key, response in newTree.items():
        #     newTree[key] = sorted(response, key=lambda newNode: newNode[0])
        return table_entries


    def getResponses(self, responseFolder):
        logger.debug(f'Get responses from {responseFolder}')
        responses = FlatDict()
        responseFileSet = set(os.listdir(responseFolder))
        successFile = 'success.json.erb'
        responseFileSet.discard(successFile)
        responseFiles = [successFile] + sorted(list(responseFileSet))

        for filename in responseFiles:
            logger.debug(f'\tfilename: {filename}')
            jsonInput = open(os.path.join(responseFolder, filename), 'r').read()
            try:
                response = FlatDict(json.loads(jsonInput))
                responses[filename] = RESPONSE_ENTRY(response['status']=='SUCCESS', response['status'].upper()=='SUCCESS', response, response.getKeys(), 'json')
            except:
                description = f'Folder: {responseFolder}/{filename} format is unsupported'
                PopupDialog(self, 'Error Disco Response Manager',
                            description)

                logger.debug(f'problem with file {filename}')
        return responses

    def renderTree2(self, all_responses):
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
        self.responses = responses
        def heading(column):
            logger.debug(f"click! {column}")

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
        tree_entries = {}
        for treeI in range(len(tree_list[successResponse])):
            parent_last = ''
            values = []
            tags = []
            for treeEntry in tree_list:
                if treeI < len(tree_list[treeEntry]):
                    values.append(tree_list[treeEntry][treeI][4])
                    # tags.append(tree_list[treeEntry][treeI][5])
            if tree_list[successResponse][treeI][0] == '':
                parent_next = f'{tree_list[successResponse][treeI][2]}'
            else:
                parent_next = f'{tree_list[successResponse][treeI][0]}:{tree_list[successResponse][treeI][2]}'
            # parent_next = f'{tree_list[successResponse][treeI][0]}:{name}'
            if tree_list[successResponse][treeI][4] is None:
                logger.debug(f'add: {tree_list[successResponse][treeI]}, {tags}, {parent_next}')
                try:
                    # tree_entries[parent_last] = self.insert(tree_list[successResponse][treeI][0],
                    tree_entries[parent_next] = self.insert(tree_entries[parent_last],
                                'end',
                                # name,
                                text=tree_list[successResponse][treeI][2],
                                tags=tags)
                except tkinter.TclError as e:
                    pass
            else:
                logger.debug(f'add: {tree_list[successResponse][treeI]}, {tags}, {parent_next}, {values}')
                try:
                    # tree_entries[parent_last] = self.insert(tree_list[successResponse][treeI][0],
                    tree_entries[parent_next] = self.insert(tree_entries[parent_last],
                                                            'end',
                                # name,
                                text=tree_list[successResponse][treeI][2],
                                tags=tags,
                                values=values)
                except tkinter.TclError as e:
                    pass
            parent_last = parent_next
        pass

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
        self.responses = responses
        def heading(column):
            logger.debug(f"click! {column}")

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
