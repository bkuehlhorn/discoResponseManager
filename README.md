##Disco Response Manager
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

###flatDict
Sub-class of `dict` to support nexted `dict` and `list`. 

###discoResponse
Render files in response folder. Highlight rows with value different from  `success`.
Uses Python tkinker.

###Next Features
- Add hide tag to File column heading.
- Aded menu items:
  - Hide / Show files with column hide tag
  - Show Success response files
  - Show Failure response files
- Show Failure response files with no value highlighting.
- Double click on row heading to update values in all shown response files from `success`
- Double click on cell to update value as one of other values or end new value
- Doucle click on column header to open file in editor (configurable)

### Who do I talk to? ###

* [Bernard Kuehlhorn](mailto:bkuehlhorn@acm.org)