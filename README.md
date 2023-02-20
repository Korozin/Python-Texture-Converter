# Python-Texture-Converter

---
### Python CLI Usage and Documentation

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
