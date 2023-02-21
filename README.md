# Python CLI Usage and Documentation

#### Help Message
```
usage: PyConvert-CLI.py [-h] [-items <zip path>] [-blocks <zip path>] [-armor <zip path>] [-environment <zip path>]
               [-particles <zip path>] [-fire <zip path>] [-misc <zip path>] [-all <zip path>]

Convert 1.8 Texture Packs to Legacy Console

options:
  -h, --help            show this help message and exit
  -items <zip path>, --convert_items <zip path>
                        Converts only items
  -blocks <zip path>, --convert_blocks <zip path>
                        Converts only blocks
  -armor <zip path>, --convert_armor <zip path>
                        Converts only armor
  -environment <zip path>, --convert_environment <zip path>
                        Converts only environment / terrain
  -particles <zip path>, --convert_particles <zip path>
                        Converts only particles
  -fire <zip path>, --convert_fire <zip path>
                        Converts only fire
  -misc <zip path>, --convert_misc <zip path>
                        Converts only misc items
  -all <zip path>, --convert_all <zip path>
                        Converts everything
```
#### Usage Example
```
PyConvert-CLI.py -all pack.zip
```

#### Documentation
The program will now unzip the contents of a zipped Texture Pack into a temporary folder to search through in order to convert, rename and move the files in question to be compatible with the Legacy Console format. This change was made for several reasons including but not limited to cleanliness, user accessability, and to refrain from using static input methods. Both the temporary folder and `fallback.zip` will be deleted after relevant use, so don't worry about bloating.

The method of logging operations has also been cleaned to show what operation is happening, under what name it's happening, and what is being done with it. For example the outputs below will detail a fully passed, fallback passed, and skipped conversion.

```
[normal]: leather_helmet.png pasted to (0, 0)
[fallback]: leather_helmet.png pasted to (0, 0)
[skipped]: leather_helmet.png not found ... Skipping
```

They will also be color-coded in the Terminal output for easier reading.

See comments for more relevant code information.

---

# Python GUI Usage and Documentation

## Dependencies:
- PyQt5
- Pillow _(should come with base Python)_
- shutil _(should come with base Python)_
- argparse _(should come with base Python)_
- requests _(should come with base Python)_

## To download dependencies

```cmd
pip install <package_name>
```
Windows Executables are already pre-packed with the dependencies, so they can be used out-the-box.

### On-Start documentation

Upon running the application for the first time you will be greeted with the message `Fallback directory not detected!`, it will also provide a prompmt asking if the user would like to download it. Selecting `Yes` will prompt the program to download `fallback.zip` from the link [`https://korozin.github.io/files/fallback.zip`](https://korozin.github.io/files/fallback.zip). The program will the unzip the contents `fallback.zip` into the directory `fallback`, and it will be used to replace missing images. However, if the user chooses `No`, it will simply move on and allow the user to convert Texture Packs without the use of the `fallback` feature. 

#### Image Example of `fallback` dialog
<img src="https://user-images.githubusercontent.com/90534409/220387886-31d35a41-986b-43ba-b8e3-5b0111c65a6a.png" width="300px" height="140px">

### Conversion Tab documentation

Once in the main area, the user will have two fields before them. One is for the `Input` and another is for the `Output`. The `Input` field should be populated with the Path of the ZIPPED Texture Pack, as well as being able to type it manually, there is a button with the text `...` that allows the User to select the Path from a GUI. If the user leaves the `Input` field empty, no operations will be run and it will throw an Error Dialog.

The `Output` field is a bit more forgiving. If left empty then it will auto-set the used directory to a folder named `Output`, and if it doesn't exist, it will create it. This means that the `Output` field is actually optional, but if you'd like to set a custom name to it, or make sure the Converted contents are put into a specific folder- you can do so.

The `Start` button will simply start the conversion process

#### Image Example of `Conversion` tab 
<img src="https://user-images.githubusercontent.com/90534409/220390231-d4e30824-1dea-4726-88a6-580a9a1a4a5c.png" width="260px" height="240px">

### Options Tab documentation

The `Options` tab has an array of checkboxes to determine what will and will not be converted. If a checkbox is enabled, then the Conversion Function associated will be run. If not, then it will pass.

The `Download Fallback` button will allow the user to manually download and unzip `fallback.zip`. If the `fallback` directory already exists, then it will be deleted and replaced with a new one.

The `fallback : ` label will display the status of the `fallback` directory. If the `fallback` directory does not exist, it will be `missing`, if it does exist it will be `detected`. The function that updates the label is tied to a `QTimer` instance, so it will update in real-time.

#### Image Example of `Options` tab
<img src="https://user-images.githubusercontent.com/90534409/220392398-f2423071-f426-4e1f-aa68-2805a45835fc.png" width="260px" height="240px">

### Log Tab documentation

The `Log` tab contains a uneditable `QTextEdit` widget which houses the Terminal output of the program. That includes [normal], [fallback], [skip], and [log] operations. The tab also includes a `Clear Log` button, which will simply clear the log, and another `Start` button in-case the user would like to start the Conversion from the `Log` tab.

#### Image Example of `Log` tab
<img src="https://user-images.githubusercontent.com/90534409/220393567-c745c38a-8369-4f39-8de1-873d265cf16c.png" width="260px" height="240px">

## Video of usage example
<!-- [![Alt text](https://img.youtube.com/vi/epHbc041cTg/0.jpg)](https://www.youtube.com/watch?v=epHbc041cTg) -->
https://user-images.githubusercontent.com/90534409/220401816-24e709db-0a3a-409a-a501-98af0a8fefc0.mp4
