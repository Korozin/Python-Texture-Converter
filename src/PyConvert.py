import os, shutil, requests, zipfile
from PyQt5 import QtWidgets, QtGui, QtCore
from Classes import MainWindow, ImageCreator, FileMover, TextureExtractor, FileMaps, ErrorWindow, InfoWindow


class InvalidDataInput(Exception):pass


class PyConvert_Main(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(PyConvert_Main, self).__init__()

        # Set up clock
        self.Timer = QtCore.QTimer()
        self.Timer.start(1000) # Set timer to 1 second

        # Set up base GUI parameters
        self.setupUi(self)
        self.Set_Functions()

        self.ItemsRes_comboBox.addItems(["16x", "32x"])
        self.BlocksRes_comboBox.addItems(["16x", "32x"])
        self.Version_comboBox.addItems(["1.8", "1.13+"])

        # Initialize Error / Info windows
        self.ErrorWindow = ErrorWindow.ErrorWindow()
        self.InfoWindow = InfoWindow.InfoWindow()

    def Set_Functions(self):
        self.Browse_pushButton.clicked.connect(self.Browse_Input)
        self.Browse_pushButton_2.clicked.connect(self.Browse_Output)
        self.Start_pushButton.clicked.connect(lambda: self.Start_Conversion(self.Input_lineEdit.text(), self.Output_lineEdit.text()))
        self.Check_pushButton.clicked.connect(lambda: self.Check_Settings(True))
        self.Uncheck_pushButton.clicked.connect(lambda: self.Check_Settings(False))
        self.Fallback_pushButton.clicked.connect(self.Download_Fallback)
        self.Timer.timeout.connect(self.Update_Fallback_Label)

    def Browse_Input(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select ZIP file", "", "ZIP Files (*.zip)", options=options)
    
        if file_path:
            self.Input_lineEdit.setText(file_path)


    def Browse_Output(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)

        if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
            selected_directory = dialog.selectedFiles()[0]
            self.Output_lineEdit.setText(selected_directory)

    def Check_Settings(self, state):
        self.Fallback_checkBox.setChecked(state)
        self.Items_checkBox.setChecked(state)
        self.Blocks_checkBox.setChecked(state)
        self.Armor_checkBox.setChecked(state)
        self.Fire_checkBox.setChecked(state)
        self.Particles_checkBox.setChecked(state)
        self.Misc_checkBox.setChecked(state)

    def Download_Fallback(self):
        try:
            if not os.path.exists("fallback"):
                if os.path.exists("fallback.zip"):
                    with zipfile.ZipFile("fallback.zip", "r") as zip_ref:
                        zip_ref.extractall("fallback")
                    os.remove('fallback.zip')
                else:
                    url = "https://korozin.github.io/assets/downloads/textures/fallback.zip"
                    response = requests.get(url)
                    open("fallback.zip", "wb").write(response.content)
                    with zipfile.ZipFile("fallback.zip", "r") as zip_ref:
                        zip_ref.extractall("fallback")
                    os.remove('fallback.zip')
            else:
                shutil.rmtree("fallback")
                self.Download_Fallback()
        except Exception as e:
                self.ErrorWindow.CreateWindow("Error!",
                                             f"{e}\n\nMaybe the fallback download is invalid or corrupted?",
                                             500, 200)
                self.ErrorWindow.show()

    def Update_Fallback_Label(self):
        if not os.path.exists("fallback"):
            self.Fallback_Label.setText("fallback : <span style='color:red'>missing</span>")
        else:
            self.Fallback_Label.setText("fallback : <span style='color:#00f500'>detected</span>")

    def Calc_Image_Size(self, rows, num_of_rows, img_size):
        size = (rows * img_size), ((num_of_rows * img_size) // rows)
        return size

    def Convert_Items(self, Version, Output_Path):
        Coord_Spacing = self.ItemsRes_comboBox.currentText()

        if Coord_Spacing == "16x":
            Coord_Spacing = 16
        elif Coord_Spacing == "32x":
            Coord_Spacing = 32
        elif Coord_Spacing == "":
            raise InvalidDataInput("Item Resolution field CANNOT be left empty!")
        else:
            raise InvalidDataInput("Invalid Items res data!")

        Calculated_Image = self.Calc_Image_Size(16, 272, int(Coord_Spacing))
        Image_Size = (Calculated_Image[0], Calculated_Image[1])
        Unified_Size = Calculated_Image[0] + Calculated_Image[1]

        if self.Fallback_checkBox.isChecked():
            if Version == "1.8":
                if Unified_Size == 528:
                    Fallback_Path = "./fallback/1.8/16x/items"
                elif Unified_Size == 1056:
                    Fallback_Path = "./fallback/1.8/32x/items"
            elif Version == "1.13+":
                if Unified_Size == 528:
                    Fallback_Path = "./fallback/1.13+/16x/items"
                elif Unified_Size == 1056:
                    Fallback_Path = "./fallback/1.13+/32x/items"
        else:
            Fallback_Path = None

        Items_Input = './temp/items' if Version == "1.8" else './temp/item'
        Items_Map = FileMaps.Java_Items_1_8 if Version == "1.8" else FileMaps.Java_Items_1_13
        Items_Creator = ImageCreator.ImageCreator(Items_Input, Items_Map, Image_Size, int(Coord_Spacing), Fallback_Path)
        Items_Image = Items_Creator.create_image()
        Items_Image.save(Output_Path + "/items.png")

    def Convert_Blocks(self, Version, Output_Path):
        Coord_Spacing = self.BlocksRes_comboBox.currentText()

        if Coord_Spacing == "16x":
            Coord_Spacing = 16
        elif Coord_Spacing == "32x":
            Coord_Spacing = 32
        elif Coord_Spacing == "":
            raise InvalidDataInput("Terrain Resolution field CANNOT be left empty!")
        else:
            raise InvalidDataInput("Invalid Terrain res data!")

        Calculated_Image = self.Calc_Image_Size(16, 544, int(Coord_Spacing))
        Image_Size = (Calculated_Image[0], Calculated_Image[1])
        Unified_Size = Calculated_Image[0] + Calculated_Image[1]
        mipMap2_Size = (Image_Size[0] // 2, Image_Size[1] // 2)
        mipMap3_Size = (Image_Size[0] // 4, Image_Size[1] // 4)

        if self.Fallback_checkBox.isChecked():
            if Version == "1.8":
                if Unified_Size == 800:
                    Fallback_Path = "./fallback/1.8/16x/blocks"
                elif Unified_Size == 1600:
                    Fallback_Path = "./fallback/1.8/32x/blocks"
            elif Version == "1.13+":
                if Unified_Size == 800:
                    Fallback_Path = "./fallback/1.13+/16x/blocks"
                elif Unified_Size == 1600:
                    Fallback_Path = "./fallback/1.13+/32x/blocks"
        else:
            Fallback_Path = None

        Blocks_Input = './temp/blocks' if Version == "1.8" else './temp/block'
        Blocks_Map = FileMaps.Java_Blocks_1_8 if Version == "1.8" else FileMaps.Java_Blocks_1_13
        Blocks_Creator = ImageCreator.ImageCreator(Blocks_Input, Blocks_Map, Image_Size, int(Coord_Spacing), Fallback_Path)
        Blocks_Image = Blocks_Creator.create_image()
        Blocks_Image.save(Output_Path + "/terrain.png")

        mipMapLevel2 = Blocks_Image.resize((mipMap2_Size[0], mipMap2_Size[1]))
        mipMapLevel2.save(Output_Path + '/terrainMipMapLevel2.png')

        mipMapLevel3 = Blocks_Image.resize((mipMap3_Size[0], mipMap3_Size[1]))
        mipMapLevel3.save(Output_Path + '/terrainMipMapLevel3.png')

    def Convert(self, Input_Path, Output_Path, Fallback_Path, File_Map):
        if self.Fallback_checkBox.isChecked():
            Fallback_Path = Fallback_Path
        else:
            Fallback_Path = None

        creator = FileMover.FileMover(Input_Path, Fallback_Path, Output_Path, File_Map)
        creator.convert()

    def Start_Conversion(self, Input_Path, Output_Path):
        try:
            if Input_Path == "":
                raise InvalidDataInput("The Input Path field CANNOT be left empty!")

            Version = self.Version_comboBox.currentText()

            Extractor = TextureExtractor.TextureExtractor(Version, Input_Path, "temp")
            Extractor.extract_textures()

            if Output_Path == "":
                Output_Path = "./Output"

            if not os.path.exists(Output_Path):
                os.mkdir(Output_Path)

        

            Fire_Path = "./temp/blocks" if Version == "1.8" else "./temp/block"
            Fire_Map = FileMaps.Java_Fire_1_8 if Version == "1.8" else FileMaps.Java_Fire_1_13

            Convert_Methods = [
                (self.Items_checkBox.isChecked, self.Convert_Items, [Version, Output_Path]),
                (self.Blocks_checkBox.isChecked, self.Convert_Blocks, [Version, Output_Path]),
                (self.Armor_checkBox.isChecked, self.Convert, ['./temp/models/armor', Output_Path + "/armor", "./fallback/Static/armor", FileMaps.Java_Armor]),
                (self.Fire_checkBox.isChecked, self.Convert, [Fire_Path, Output_Path + "/fire", "./fallback/Static/fire", Fire_Map]),
                (self.Particles_checkBox.isChecked, self.Convert, ['./temp/particle', Output_Path, "./fallback/Static/particle", FileMaps.Java_Particles]),
                (self.Misc_checkBox.isChecked, self.Convert, ['./temp/environment', Output_Path + "/environment", "./fallback/Static/environment", FileMaps.Java_Environment]),
                (self.Misc_checkBox.isChecked, self.Convert, ['./temp/misc', Output_Path + "/misc", "./fallback/Static/misc", FileMaps.Java_Misc])
            ]

            for Check_Func, Convert_Func, Args in Convert_Methods:
                if Check_Func():
                    Convert_Func(*Args)

            shutil.rmtree("./temp")

            self.InfoWindow.CreateWindow("Process Completed!",
                                 f"Successfully completed conversion of '{os.path.basename(Input_Path)}' into '{os.path.basename(Output_Path)}'!",
                                 500, 200)
            self.InfoWindow.show()
        except Exception as e:
            self.ErrorWindow.CreateWindow("Error!",
                                         f"{e}<br/><br/>Invalid or empty Input Fields!",
                                         500, 200)
            self.ErrorWindow.show()


if __name__ == "__main__":
    import sys
    PyConvert_App = QtWidgets.QApplication(sys.argv)
    PyConvert_Var = PyConvert_Main()
    PyConvert_Var.show()
    sys.exit(PyConvert_App.exec_())
