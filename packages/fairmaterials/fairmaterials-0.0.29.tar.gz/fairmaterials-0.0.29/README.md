# Fairmaterials

Fairmaterials is a tool for fairing data. It reads a template JSON file to get the preset data. The user can edit the data by manually inputting or by importing a csv file. The final output will be a new JSON file with the same structure. 


# Features
 -  Importing JSON template as JSON-LD
 -   Display fair data in dataframe format
 -   Automatically notify duplicate names
 -   Modify JSON data
		- Based on CSV file
		- Based on keyboard input
 -   Output as standard JSON-LD

#  A quick example
***Load a template file***
```python
device=fairjson('cots_json_template.json')
``` 
***Display the data***
```python
device.display_current_JSONDF()
``` 
***Load CSV file***
```python
device.importCsv('data.csv')
``` 
***Check the detailed description of the key***
```python
device.searchKey('scbi')
``` 
***Change the value of "scbi" to "testvalue"*** 
```python
device.setValue('scbi','testvalue')
``` 
***Save to JSON file***
```python
device.save_to_json('test.json')
``` 



