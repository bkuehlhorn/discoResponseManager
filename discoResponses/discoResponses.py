

import json
import os

import tkinter
import tkinter.ttk as ttk
from flatDict.flatDict import *
from discoResponseManager import  logger

FLATKEYSDEPTH = collections.namedtuple('FLATKEYSDEPTH', 'level text0 keys items')
RESPONSE_ENTRY = collections.namedtuple('RESPONSE_ENTRY', 'success show response, allKeys')

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
            self.button = ttk.Button(self.top, text=_("OK"), command=self.ok_button)
            self.button.grid(row=3, column=1, pady=5)

            logger.debug(f'popug: {(row, column, value)}')

        def ok_button(self):
            "OK button feedback."
            logger.debug('ok button hit')
            self.value = self.e.get()
            logger.debug(f'values: {self.value}')
            """.set(iid, column=None, value=None)
            Use this method to retrieve or set the column values of the item specified by iid. With one argument, the method returns a dictionary: the keys are the column identifiers, and each related value is the text in the corresponding column.
            
            With two arguments, the method returns the data value from the column of the selected item whose column identifier is the column argument. With three arguments, the item's value for the specified column is set to the third argument.
            """
            self.top.destroy()
            self.master.set(self.master.rowid, self.master.columnid, self.value)
            pass

    # def popup(self):
    #     self.w = self.popupWindow(self)
    #     self.b["state"] = "disabled"
    #     self.master.wait_window(self.w.top)
    #     self.b["state"] = "normal"

    def callback(self, event):
        rowid = self.identify_row(event.y)
        column = self.identify_column(event.x)
        selItems = self.selection()
        # col = int(column[1]) - 1
        if rowid == '':
            logger.debug('Click on header')
        else:
            logger.debug(f'Click on row: {rowid}')
            _description = _('promptd to replace all shown None values with selected or entered value.')
            # self.PopupUpdateValue(self, 'Disco Response Manager - Row Update:', _description, rowid, column, selItems)

        if column == '#0':
            logger.debug('Cell data:', 'row heading: ', selItems)
        else:
            # logger.debug(f'Cell data: column heading: {self["column"][column]}')
            _description = _('promptd to edit or save response. hide or show response file.')
            self.rowid = rowid
            self.columnid = column
            self.PopupUpdateValue(self, 'Disco Response Manager - Column Update', _description, rowid, column, selItems)
        if selItems:
            # selItem = selItems[0]
            text = self.set(rowid, column)
            # textPrint = set(text)
            # textPrint.discard('None')
            logger.debug(f'Row data: {text}')
            if column == '#0':
                logger.debug('no cell reference')
            else:
                logger.debug(f'Clicked on Collumn: {col}')
                logger.debug(f'Column data: {text}')
        else:
            logger.debug(f'Clicked on Column: {col}')
            logger.debug('Column heading')


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


    def insertTree(self, flatKeys, responses):
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
            flatKeyParts = flatKey.split(':')
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
                        text0 = 'something'
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
            jsonInput = jsonInput.replace('<%', '"<%')
            jsonInput = jsonInput.replace('%>', '%>"')
            try:
                response = FlatDict(json.loads(jsonInput))
                responses[filename] = RESPONSE_ENTRY(response['status']=='SUCCESS', response['status'].upper()=='SUCCESS', response, response.getKeys())
            except:
                description = f'Folder: {responseFolder}/{filename} format is unsupported'
                PopupDialog(self, 'Error Disco Response Manager',
                            description)

                logger.debug(f'problem with file {filename}')
        return responses

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
        for treeI in range(len(tree_list[successResponse])):
            values = []
            tags = []
            for treeEntry in tree_list:
                if treeI < len(tree_list[treeEntry]):
                    values.append(tree_list[treeEntry][treeI][4])
                    # tags.append(tree_list[treeEntry][treeI][5])
            if tree_list[successResponse][treeI][0] == '':
                name = f'{tree_list[successResponse][treeI][2]}'
            else:
                name = f'{tree_list[successResponse][treeI][0]}:{tree_list[successResponse][treeI][2]}'
            if tree_list[successResponse][treeI][4] is None:
                logger.debug(f'add: {tree_list[successResponse][treeI]}, {tags}, {name}')
                try:
                    self.insert(tree_list[successResponse][treeI][0],
                                'end',
                                name,
                                text=tree_list[successResponse][treeI][2],
                                tags=tags)
                except tkinter.TclError as e:
                    pass
            else:
                logger.debug(f'add: {tree_list[successResponse][treeI]}, {tags}, {name}, {values}')
                try:
                    self.insert(tree_list[successResponse][treeI][0],
                                'end',
                                name,
                                text=tree_list[successResponse][treeI][2],
                                tags=tags,
                                values=values)
                except tkinter.TclError as e:
                    pass
