# **wrapup**

This is a python library that will help you to **remove print statements** or **convert the quotes** of python files based on your given input. You have to input the path of the file or folder, and if the filepath is correct then the changes will be applied to all the python files in the folder or the file whose path was added.

<br />

**IMPORTANT NOTES TO CONSIDER**: 
1. In case if path of folder is passed as parameter, then the changes will be applied to all the python files (if possible) in the folder.
2. **No changes** will be made to the python file, if by any chance removing print statement or converting the quotes leads to some _syntactical errors_.

<br />

To install the library, type in the command line:
```pip install wrapup```

Import the package using: ```import wrapup```

## Usage:

* To remove print statements from the files, use **rmv_print** function which takes the following arguments:

  1. **filepath**: The path of the file to be provided. The path can be relative or absolute. (If not provided; current working directory is considered)

  2. **rmv_main**: (_default_: False) Boolean value if True then, print statements should be removed from the main function _main( )_ or under <br />```if __name__ == "__main__":``` 

  3. **rmv_root**: : (_default_: False) Boolean value if True then, print statements from _level 0 indentations_ will be removed 
     
  4. **funcs_to_spare**: Optional argument of _list_ type that will ignore the functions specified in the list (not removing the print statements from the specified functions)
   
   **Return value of the function is a list of path of python files to which changes were applied.**
   
   <br />


<br />
<br />

* To convert single quotes to double quotes or vices versa, use **convert_quotes** function which takes the following arguments:

  1. **filepath**: The path of the file to be provided.
   The path can be relative or absolute. (If not provided; current working directory is considered)
   
  2. **single**: (_default_: True) Boolean value if True, convert all the quotes of the file to single quotes and to double quotes if False

     **Return value of the function is a list of path of python files to which changes were applied.**
       
  The below example will convert all the quotes of all the python files in the _folder_ (subsequently in all sub-folders) to double quotes,
  ```
  from wrapup import convert_quotes
  convert_quotes(filepath="folder", single=False)
  ```