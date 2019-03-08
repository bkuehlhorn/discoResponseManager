## Disco Response Manager
### Purpose
Support for response files in Disco endpoint folders. Loads all scenario
files and renders Success files for comparing and updating. Entries are easy
to check across all Success scenario files. Values can be updated as needed.
Current implementation does not support adding or deleting values.

There is no support for complex interpolation. Only simple string values are supported.

Endpoint Folder contains files of JSON data used to test API.
Each file is part of a scenario with other Endpoint folders.
Each file consists of nested `dict` and `list` entries. 
Files are `success` or `falure`. `sucess` files are render and values
Success file is the master.
Row is highlighted when values do not match `success` file

Endpoint Folder

: location for all scenario files to support Endpoint requests

Response File

: JSON response text to give response data. 

###Install
Install python 3.6 or higher
Install pipenv
Clone repository and run `pipenv` to configure libraries.

.bash_profile update for easy use:

`alias 'discoResponseManager='python ~/discoResponseManager/discoResponseManager.py '`

### flatDict
Sub-class of `dict` to support nexted `dict` and `list`. 
* getValue(self, key): key is a string to access an element.
* addValue(self, key, value): key is a string to access an element, value to update element
* getKeys(self): returns list of all keys to access elements


### discoResponse
Render files in response folder. Highlight rows with value different from  `success`.
Uses Python tkinker.

Double click on value: if not None: pop up frame to enter new value.
Double click on column file name: pop up frame to save values

### Next Features
- Add hide tag to File column heading.
- Aded menu items:
  - Hide / Show files with column hide tag
  - Show Success response files
  - Show Failure response files
- Show Failure response files with no value highlighting.
- Double click on row heading to update values in all shown response files from `success`

### Who do I talk to? ###

* [Bernard Kuehlhorn](mailto:bkuehlhorn@acm.org)