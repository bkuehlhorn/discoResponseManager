

import json
import os

import tkinter
import tkinter.ttk as ttk
from flatDict.flatDict import *

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


class discoTree(ttk.Treeview):
    responses = []

    def popup(self):
        self.w = self.popupWindow(self)
        self.b["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.b["state"] = "normal"

    def callback(self, event):
        rowid = self.identify_row(event.y)
        column = self.identify_column(event.x)
        selItems = self.selection()
        col = int(column[1]) - 1
        if rowid == '':
            print('Click on header')
        else:
            print('Click on row:', rowid)
            _description = _('promptd to replace all shown None values with selected or entered value.')
            PopupDialog(self, 'Disco Response Manager - Row Update', _description)

        if col == -1:
            print('Cell data:', 'row heading: ', selItems)
        else:
            print('Cell data:', 'column heading: ', self['column'][col])
            _description = _('promptd to edit or save response. hide or show response file.')
            PopupDialog(self, 'Disco Response Manager - Column Update', _description)
        if selItems:
            selItem = selItems[0]
            text = self.item(selItem, 'values')
            textPrint = set(text)
            textPrint.discard('None')
            print('Row data:', textPrint)
            if col == -1:
                print('no cell reference')
            else:
                print('Clicked on Collumn:', col)
                if len(text) > 0:
                    print('Column data:', text[col])
                else:
                    print('Column heading')
        else:
            print('Clicked on Column:', col)
            print('Column heading')


    def __init__(self, parent, responseFolder):
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
            for responseToken in responses:
                tagL = ''
                stackI = 0
                removeKeys = True
                for newPart in flatKeyParts:
                    if removeKeys:
                        if stackI < len(value[responseToken].keys) and value[responseToken].keys[stackI] == newPart:
                            stackI += 1
                        else:
                            del value[responseToken].keys[stackI:]
                            del value[responseToken].items[stackI:]
                            removeKeys = False
                    if not removeKeys: # not else. need to process newPart not in value[responseToken].keys
                        if newPart.isnumeric():
                            newPart = int(newPart)
                        if len(value[responseToken].items) == 0:
                            value[responseToken].items.append(responses[responseToken].response[newPart])
                        else:
                            if tagL == '' and newPart in value[responseToken].items[-1]:
                                value[responseToken].items.append(value[responseToken].items[-1][newPart])
                            else:
                                tagL = 'missing'
                        item = ':'.join(value[responseToken].keys)
                        value[responseToken].keys.append(newPart if isinstance(newPart, str) else str(newPart))
                        text0 = 'something'
                        if isinstance(value[responseToken].items[-1], (dict, list)):
                            newTree[responseToken].append((item, 'end', newPart, newPart, None, tagL))
                        else:
                            newTree[responseToken].append((item, 'end', newPart, newPart, (value[responseToken].items[-1]), tagL))

            pass
        return newTree


    def getResponses(self, responseFolder):
        responses = FlatDict()
        responseFileSet = set(os.listdir(responseFolder))
        successFile = 'success.json.erb'
        responseFileSet.discard(successFile)
        responseFiles = [successFile] + sorted(list(responseFileSet))

        for filename in responseFiles:
            response = FlatDict(json.load(open(os.path.join(responseFolder, filename), 'r')))
            responses[filename] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys())
        return responses

    def renderTree(self, responses):
        """
        Use

        create table for self:
        walk each response.response[]... to get value for column list

        :param self:
        :param responses:
        :return:
        """
        self.responses = responses
        def heading(column):
            print(f"click! {column}")

        successResponse = list(responses.keys())[0]
        columns = list(responses.keys())
        self["columns"] = columns
        self["displaycolumns"] = columns
        self.column(successResponse, width=200)
        for title in columns:
            self.heading(title, text=title)

        treeList = self.insertTree(responses[successResponse].allKeys, responses)
        for treeI in range(len(treeList[successResponse])):
            values = []
            tags = []
            for treeEntry in treeList:
                values.append(treeList[treeEntry][treeI][4])
                tags.append(treeList[treeEntry][treeI][5])
            if treeList[successResponse][treeI][4] is None:
                self.insert(treeList[successResponse][treeI][0], 'end', treeList[successResponse][treeI][2], text=treeList[successResponse][treeI][2], tags=tags)
            else:
                self.insert(treeList[successResponse][treeI][0], 'end', treeList[successResponse][treeI][2], text=treeList[successResponse][treeI][2], values=values, tags=tags)
