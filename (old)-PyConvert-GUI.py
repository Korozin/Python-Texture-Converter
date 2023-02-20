import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import *
from PIL import Image
import zipfile
import requests
import shutil

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_folder = ""
        self.output_folder = ""

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Texture Converter : KorOwOzin")
        self.setFixedSize(470, 380)

        # Create tab widget
        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create input/output tab
        self.input_output_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.input_output_tab, "Input/Output")
        self.input_output_layout = QtWidgets.QVBoxLayout(self.input_output_tab)

        # Create input folder line edit and browse button
        self.input_folder_line_edit = QtWidgets.QLineEdit()
        self.input_folder_line_edit.setPlaceholderText("Input folder location")
        self.input_folder_line_edit.setToolTip("Set the location of the input folder")
        self.input_folder_browse_button = QtWidgets.QPushButton("Browse")
        self.input_folder_browse_button.setToolTip("Select the input folder that contains your texture pack from GUI")
        self.input_folder_browse_button.clicked.connect(self.select_input_folder)
        input_folder_layout = QtWidgets.QHBoxLayout()
        input_folder_layout.addWidget(self.input_folder_line_edit)
        input_folder_layout.addWidget(self.input_folder_browse_button)
        self.input_output_layout.addLayout(input_folder_layout)

        # Create output folder line edit and browse button
        self.output_folder_line_edit = QtWidgets.QLineEdit()
        self.output_folder_line_edit.setPlaceholderText("Output folder location")
        self.output_folder_line_edit.setToolTip("Set the Output folder location")
        self.output_folder_line_edit.setText(self.output_folder)
        self.output_folder_browse_button = QtWidgets.QPushButton("Browse")
        self.output_folder_browse_button.setToolTip("Select Output folder from GUI")
        self.output_folder_browse_button.clicked.connect(self.select_output_folder)
        output_folder_layout = QtWidgets.QHBoxLayout()
        output_folder_layout.addWidget(self.output_folder_line_edit)
        output_folder_layout.addWidget(self.output_folder_browse_button)
        self.input_output_layout.addLayout(output_folder_layout)

        # Create start button on input/output tab
        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.setToolTip("Start Conversion")
        self.start_button.clicked.connect(self.start_conversion)
        self.input_output_layout.addWidget(self.start_button)

        # Create options tab
        self.options_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.options_tab, "Options")
        self.options_layout = QtWidgets.QVBoxLayout(self.options_tab)

        # Create fallback checkbox
        self.fallback_checkbox = QtWidgets.QCheckBox("Use fallback images")
        self.fallback_checkbox.setToolTip("Select whether or not fallback images are used")
        self.options_layout.addWidget(self.fallback_checkbox)
        self.fallback_checkbox.setChecked(True)

        # Create items checkbox
        self.items_checkbox = QtWidgets.QCheckBox("Convert items")
        self.items_checkbox.setToolTip("Select whether or not Items are converted")
        self.options_layout.addWidget(self.items_checkbox)
        self.items_checkbox.setChecked(True)

        # Create blocks checkbox
        self.blocks_checkbox = QtWidgets.QCheckBox("Convert blocks")
        self.blocks_checkbox.setToolTip("Select whether or not Blocks are converted")
        self.options_layout.addWidget(self.blocks_checkbox)
        self.blocks_checkbox.setChecked(True)
        
        # Create particles checkbox
        self.particles_checkbox = QtWidgets.QCheckBox("Convert particles")
        self.particles_checkbox.setToolTip("Select whether or not Particles are converted")
        self.options_layout.addWidget(self.particles_checkbox)
        self.particles_checkbox.setChecked(True)
        
        # Create armor checkbox
        self.armor_checkbox = QtWidgets.QCheckBox("Convert armor")
        self.armor_checkbox.setToolTip("Select whether or not Armor is converted")
        self.options_layout.addWidget(self.armor_checkbox)
        self.armor_checkbox.setChecked(True)
        
        # Create environment checkbox
        self.environment_checkbox = QtWidgets.QCheckBox("Convert environment")
        self.environment_checkbox.setToolTip("Select whether or not Environment files are converted")
        self.options_layout.addWidget(self.environment_checkbox)
        self.environment_checkbox.setChecked(True)

        # Create download fallback button
        self.download_fallback_button = QtWidgets.QPushButton("Download Fallback")
        self.download_fallback_button.setToolTip("Downloads fallback.zip")
        self.download_fallback_button.clicked.connect(self.download_fallback)
        self.options_layout.addWidget(self.download_fallback_button)

        # Create log tab
        self.log_tab = QtWidgets.QWidget()
        self.log_layout = QtWidgets.QVBoxLayout()
        self.log_tab.setLayout(self.log_layout)
        self.tab_widget.addTab(self.log_tab, "Log")

        # Create log text edit
        self.log_text_edit = QtWidgets.QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_layout.addWidget(self.log_text_edit)

        # Create clear log button
        self.clear_log_button = QtWidgets.QPushButton("Clear Log")
        self.clear_log_button.setToolTip("Clears the log")
        self.clear_log_button.clicked.connect(self.clear_log)
        self.log_layout.addWidget(self.clear_log_button)

        # Create start button on log tab
        self.start_button2 = QtWidgets.QPushButton("Start")
        self.start_button2.setToolTip("Starts Conversion")
        self.start_button2.clicked.connect(self.start_conversion)
        self.log_layout.addWidget(self.start_button2)
        
        ''' Create a dialog box that shows if fallback.zip isn't detected
        Gives the user the option to download it
        Dialog box only shows if fallback.zip can't be found, otherwise program runs 
        normally '''
        fallback_detected = self.check_fallback_zip()
        if fallback_detected == False:
            fallback_dialog = QtWidgets.QMessageBox()
            fallback_dialog.setWindowTitle('fallback.zip is missing!')
            fallback_dialog.setText("fallback.zip not detected! Would you like to download it now?")
            fallback_dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.center_dialog(fallback_dialog)
            choice = fallback_dialog.exec_()
            if choice == QtWidgets.QMessageBox.Yes:
                self.download_fallback()
                fallback_detected = True
        self.fallback_label = QtWidgets.QLabel()
        if fallback_detected:
            self.fallback_label.setText("fallback.zip : detected")
        else:
            self.fallback_label.setText("fallback.zip : missing")
        self.options_layout.addWidget(self.fallback_label)
        
        self.center()
        self.show()
        
    # Make the MainWindow appear in the center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    # Make the fallback_dialog appear in the center of the screen
    def center_dialog(self, dialog):
        qr = dialog.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        dialog.move(qr.topLeft())

    # Checks if fallback.zip exists, if not return Boolean
    def check_fallback_zip(self):
        if os.path.exists('fallback.zip'):
            return True
        else:
            return False

    # Downloads and Unzips fallback.zip, also updates label to reflect detection
    def download_fallback(self):
        self.log_text_edit.append("Downloading fallback.zip...")
        url = "https://github.com/Korozin/Py_MC_WiiU_Texture_Converter/blob/main/Assets/fallback.zip?raw=true"
        response = requests.get(url)
        open("fallback.zip", "wb").write(response.content)
        self.log_text_edit.append("fallback.zip downloaded.")
        if os.path.exists("fallback.zip"):
            with zipfile.ZipFile("fallback.zip", "r") as zip_ref:
                zip_ref.extractall("fallback")
                self.log_text_edit.append("fallback.zip unzipped.")
                try:
                    self.fallback_label.setText("fallback.zip : detected")
                except AttributeError:
                    self.log_text_edit.append("fallback.zip : updated")
        else:
            self.log_text_edit.append("fallback.zip not found.")
            self.check_fallback_zip()

    # Clears the Log
    def clear_log(self):
        self.log_text_edit.clear()

    # Selects the Input directory
    def select_input_folder(self):
        input_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if input_folder:
            self.input_folder_line_edit.setText(input_folder)

    # Selects the Output directory
    def select_output_folder(self):
        global output_folder
        output_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if output_folder:
            self.output_folder_line_edit.setText(output_folder)

    # Starts the Image Conversion process
    def start_conversion(self):
        global var
        self.log_text_edit.clear()
        self.input_folder = self.input_folder_line_edit.text()
        self.output_folder = self.output_folder_line_edit.text()              

        # function to convert the items
        def convert_items():    
            # list of items to be placed on the image
            items = ["leather_helmet","chainmail_helmet","iron_helmet","diamond_helmet","gold_helmet","flint_and_steel","flint","coal","string","seeds_wheat","apple","apple_golden","egg","sugar","snowball","elytra","leather_chestplate","chainmail_chestplate","iron_chestplate","diamond_chestplate","gold_chestplate","bow_standby","brick","iron_ingot","feather","wheat","painting","sugarcane","bone","cake","slimeball","broken_elytra","leather_leggings","chainmail_leggings","iron_leggings","diamond_leggings","gold_leggings","arrow","end_crystal","gold_ingot","gunpowder","bread","sign","door_wood","door_iron","blank","fireball","chorus_fruit","leather_boots","chainmail_boots","iron_boots","diamond_boots","gold_boots","stick","compass_00","diamond","redstone_dust","clay_ball","paper","book_normal","map_empty","seeds_pumpkin","seeds_melon","popped_chorus_fruit","wood_sword","stone_sword","iron_sword","diamond_sword","gold_sword","fishing_rod_uncast","clock_00","bowl","mushroom_stew","glowstone_dust","bucket_empty","bucket_water","bucket_lava","bucket_milk","dye_powder_black","dye_powder_gray","wood_shovel","stone_shovel","iron_shovel","diamond_shovel","gold_shovel","fishing_rod_cast","repeater","porkchop_raw","porkchop_cooked","fish_cod_raw","fish_cod_cooked","rotten_flesh","cookie","shears","dye_powder_red","dye_powder_pink","wood_pickaxe","stone_pickaxe","iron_pickaxe","diamond_pickaxe","gold_pickaxe","bow_pulling_0","carrot_on_a_stick","leather","saddle","beef_raw","beef_cooked","ender_pearl","blaze_rod","melon","dye_powder_green","dye_powder_lime","wood_axe","stone_axe","iron_axe","diamond_axe","gold_axe","bow_pulling_1","potato_baked","potato","carrot","chicken_raw","chicken_cooked","ghast_tear","gold_nugget","nether_wart","dye_powder_brown","dye_powder_yellow","wood_hoe","stone_hoe","iron_hoe","diamond_hoe","gold_hoe","bow_pulling_2","potato_poisonous","minecart_normal","boat","melon_speckled","spider_eye_fermented","spider_eye","potion_bottle_drinkable","potion_overlay","dye_powder_blue","dye_powder_light_blue","leather_helmet_overlay","spectral_arrow","iron_horse_armor","diamond_horse_armor","gold_horse_armor","comparator","carrot_golden","minecart_chest","pumpkin_pie","spawn_egg","potion_bottle_splash","ender_eye","cauldron","blaze_powder","dye_powder_purple","dye_powder_magenta","blank","tipped_arrow_base","dragon_breath","name_tag","lead","netherbrick","fish_clownfish_raw","minecart_furnace","charcoal","spawn_egg_overlay","blank","experience_bottle","brewing_stand","magma_cream","dye_powder_cyan","dye_powder_orange","leather_leggings_overlay","tipped_arrow_head","lingering_potion","barrier","mutton_raw","rabbit_raw","fish_pufferfish_raw","minecart_hopper","hopper","nether_star","emerald","book_writable","book_written","flower_pot","dye_powder_silver","dye_powder_white","leather_boots_overlay","beetroot","beetroot_seeds","beetroot_soup","mutton_cooked","rabbit_cooked","fish_salmon_raw","minecart_tnt","armor_stand","fireworks","fireworks_charge","fireworks_charge_overlay","quartz","map","item_frame","book_enchanted","door_acacia","door_birch","door_dark_oak","door_jungle","door_spruce","rabbit_stew","fish_salmon_cooked","minecart_command_block","acacia_boat","birch_boat","dark_oak_boat","jungle_boat","spruce_boat","prismarine_shard","prismarine_crystals","leather_horse_armor","structure_void","blank","totem_of_undying","shulker_shell","iron_nugget","rabbit_foot","rabbit_hide","blank","blank","blank","blank","blank","blank","blank","blank","dragon_charge","13","cat","blocks","chirp","far","mall","mellohi","stal","strad","ward","11","wait","cod_bucket","salmon_bucket","pufferfish_bucket","tropical_fish_bucket","leather_horse_overlay","blank","blank","blank","blank","blank","blank","kelp","dried_kelp","sea_pickle","nautilus_shell","heart_of_the_sea","turtle_helmet","scute","trident","phantom_membrane"]

            # create a new image with a transparent background
            items_image = Image.new("RGBA", (256, 272), (0, 0, 0, 0))

            # starting x and y coordinates for pasting images
            x = 0
            y = 0

            # iterate through the list of items
            if self.items_checkbox.isChecked():
                for item in items:
                    # open the image file
                    try:
                        img = Image.open(self.input_folder + "/items/" + item + ".png")
                    except FileNotFoundError:
                        if self.fallback_checkbox.isChecked():
                            try:
                                img = Image.open("fallback/items/" + item + ".png")
                                self.log_text_edit.append(f"{item}.png not found ... using fallback")
                            except FileNotFoundError:
                                self.log_text_edit.append(f"{item}.png not found ... Skipped")
                                x += 16
                                continue
                        else:
                            self.log_text_edit.append(f"{item}.png not found ... Skipped")
                            x += 16
                            continue
                    # paste the image onto the new image
                    items_image.paste(img, (x, y))
                    self.log_text_edit.append(f"{item}.png pasted to : ({x}, {y})")
                    # increment x by 16 to move to the next square
                    x += 16
                    # if x is greater than or equal to 256, reset x to 0 and increment y by 16
                    if x >= 256:
                        x = 0
                        y += 16

                # save the new image
                items_image.save(os.path.join(self.output_folder, "items.png"))
    
        # Converts Block Textures
        def convert_blocks():
            # list of blocks to be placed on the image
            blocks = ["grass_top","stone","dirt","grass_side","planks_oak","stone_slab_side","stone_slab_top","brick","tnt_side","tnt_top","tnt_bottom","web","poppy","flower_dandelion","blue_concrete","sapling_oak","cobblestone","bedrock","sand","gravel","log_oak","log_oak_top","iron_block","gold_block","diamond_block","emerald_block","redstone_block","dropper_front_horizontal","mushroom_red","mushroom_brown","sapling_jungle","red_concrete","gold_ore","iron_ore","coal_ore","bookshelf","cobblestone_mossy","obsidian","grass_side_overlay","tallgrass","dispenser_front_vertical","beacon","dropper_front_vertical","crafting_table_top","furnace_front_off","furnace_side","dispenser_front_horizontal","red_concrete","sponge","glass","diamond_ore","redstone_ore","leaves_oak","black_concrete","stonebrick","dead_bush","fern","daylight_detector_top","daylight_detector_side","crafting_table_side","crafting_table_front","furnace_front_on","furnace_top","sapling_spruce","wool_colored_white","mob_spawner","snow","ice","snow","cactus_top","cactus_side","cactus_bottom","clay","reeds","jukebox_side","jukebox_top","leaves_birch","mycelium_side","mycelium_top","sapling_birch","torch_on","door_wood_upper","door_iron_upper","ladder","trapdoor","iron_bars","farmland_wet","farmland_dry","wheat_stage_0","wheat_stage_1","wheat_stage_2","wheat_stage_3","wheat_stage_4","wheat_stage_5","wheat_stage_6","wheat_stage_7","lever","door_wood_lower","door_iron_lower","redstone_torch_on","stonebrick_mossy","stonebrick_cracked","pumpkin_top","netherrack","soul_sand","glowstone","piston_top_sticky","piston_top","piston_side","piston_bottom","piston_inner","pumpkin_stem_disconnected","rail_normal_turned","wool_colored_black","wool_colored_gray","redstone_torch_off","spruce_log","log_birch","pumpkin_side","pumpkin_face_off","pumpkin_face_on","cake_top","cake_side","cake_inner","cake_bottom","mushroom_block_skin_red","mushroom_block_skin_red","pumpkin_stem_connected","rail_normal","wool_colored_red","wool_colored_pink","repeater_off","leaves_spruce","leaves_spruce","conduit","turtle_egg","melon_side","melon_top","cauldron_top","cauldron_inner","sponge_wet","mushroom_block_skin_stem","mushroom_block_inside","vine","lapis_block","wool_colored_green","wool_colored_lime","repeater_on","glass_pane_top","chest_top","ender_chest_top","turtle_egg_slightly_cracked","turtle_egg_very_cracked","jungle_log","cauldron_side","cauldron_bottom","brewing_stand_base","brewing_stand","endframe_top","endframe_side","lapis_ore","wool_colored_brown","wool_colored_yellow","rail_golden","redstone_cross","redstone_line_horizontal","enchanting_table_top","dragon_egg","cocoa_stage_2","cocoa_stage_1","cocoa_stage_0","emerald_ore","trip_wire_source","trip_wire","end_portal_frame_eye","end_stone","sandstone_top","wool_colored_blue","wool_colored_light_blue","rail_golden_powered","blank","blank","enchanting_table_side","enchanting_table_bottom","glide_blue","item_frame","flower_pot","comparator_off","comparator_on","rail_activator","rail_activator_powered","quartz_ore","sandstone_normal","wool_colored_purple","wool_colored_magenta","rail_detector","jungle_leaves","black_concrete","planks_spruce","planks_jungle","carrots_stage_0","carrots_stage_1","carrots_stage_2","carrots_stage_3","slime","water_debug","water_debug","water_debug","sandstone_bottom","wool_colored_cyan","wool_colored_orange","redstone_lamp_off","redstone_lamp_on","stonebrick_carved","planks_birch","anvil_base","anvil_top_damaged_1","quartz_block_chiseled_top","quartz_block_lines_top","quartz_block_side","hopper_outside","rail_detector_powered","water_debug","water_debug","nether_brick","wool_colored_silver","nether_wart_stage_0","nether_wart_stage_1","nether_wart_stage_2","sandstone_carved","sandstone_smooth","anvil_top_damaged_0","anvil_top_damaged_2","chiseled_quartz_block_bottom","quartz_block_lines","quartz_block_top","hopper_inside","lava_debug","lava_debug","lava_debug","destroy_stage_0","destroy_stage_1","destroy_stage_2","destroy_stage_3","destroy_stage_4","destroy_stage_5","destroy_stage_6","destroy_stage_7","destroy_stage_8","destroy_stage_9","hay_block_side","quartz_block_bottom","hopper_top","hay_block_top","lava_debug","lava_debug","coal_block","hardened_clay","noteblock","stone_andesite","stone_andesite_smooth","stone_diorite","stone_diorite_smooth","stone_granite","stone_granite_smooth","potatoes_stage_0","potatoes_stage_1","potatoes_stage_2","potatoes_stage_3","log_spruce_top","log_jungle_top","log_birch_top","hardened_clay_stained_black","hardened_clay_stained_blue","hardened_clay_stained_brown","hardened_clay_stained_cyan","hardened_clay_stained_gray","hardened_clay_stained_green","hardened_clay_stained_light_blue","hardened_clay_stained_lime","hardened_clay_stained_magenta","hardened_clay_stained_orange","hardened_clay_stained_pink","hardened_clay_stained_purple","hardened_clay_stained_red","hardened_clay_stained_silver","hardened_clay_stained_white","hardened_clay_stained_yellow","glass_black","glass_blue","glass_brown","glass_cyan","glass_gray","glass_green","glass_light_blue","glass_lime","glass_magenta","glass_orange","glass_pink","glass_purple","glass_red","glass_silver","glass_white","glass_yellow","glass_pane_top_black","glass_pane_top_blue","glass_pane_top_brown","glass_pane_top_cyan","glass_pane_top_gray","glass_pane_top_green","glass_pane_top_light_blue","glass_pane_top_lime","glass_pane_top_magenta","glass_pane_top_orange","glass_pane_top_pink","glass_pane_top_purple","glass_pane_top_red","glass_pane_top_silver","glass_pane_top_white","glass_pane_top_yellow","double_plant_fern_top","double_plant_grass_top","double_plant_paeonia_top","double_plant_rose_top","double_plant_syringa_top","flower_tulip_orange","double_plant_sunflower_top","double_plant_sunflower_front","acacia_log","acacia_log_top","planks_acacia","leaves_acacia","leaves_acacia","prismarine_bricks","red_sand","red_sandstone_top","double_plant_fern_bottom","double_plant_grass_bottom","double_plant_paeonia_bottom","double_plant_rose_bottom","double_plant_syringa_bottom","flower_tulip_pink","double_plant_sunflower_bottom","double_plant_sunflower_bottom","dark_oak_log","dark_oak_log_top","planks_big_oak","leaves_big_oak","leaves_big_oak","dark_prismarine","red_sandstone_bottom","red_sandstone_normal","flower_allium","flower_blue_orchid","flower_houstonia","flower_oxeye_daisy","flower_tulip_red","flower_tulip_white","sapling_acacia","sapling_roofed_oak","coarse_dirt","dirt_podzol_side","dirt_podzol_top","leaves_spruce","leaves_spruce","rough_prismarine","red_sandstone_carved","red_sandstone_smooth","door_acacia_upper","door_birch_upper","door_dark_oak_upper","door_jungle_upper","door_spruce_upper","chorus_flower","chorus_flower_dead","chorus_plant","end_stone_bricks","grass_path_side","grass_path_top","barrier","ice_packed","sea_lantern","daylight_detector_inverted_top","iron_trapdoor","door_acacia_lower","door_birch_lower","door_dark_oak_lower","door_jungle_lower","door_spruce_lower","purpur_block","purpur_pillar","purpur_pillar_top","end_rod","magma","nether_wart_block","red_nether_bricks","frosted_ice_0","frosted_ice_1","frosted_ice_2","frosted_ice_3","beetroots_stage_0","beetroots_stage_1","beetroots_stage_2","beetroots_stage_3","green_cmd","green_cmd","green_cmd","green_cmd","cmd","cmd","cmd","cmd","purple_cmd","purple_cmd","purple_cmd","purple_cmd","bone_block_side","bone_block_top","melon_stem_disconnected","melon_stem_connected","observer_front","observer_side","observer_back","observer_back_on","observer_top","glide_yellow","glide_green","structure_block","structure_block_corner","structure_block_data","structure_block_load","structure_block_save","black_concrete","blue_concrete","brown_concrete","cyan_concrete","gray_concrete","green_concrete","light_blue_concrete","lime_concrete","magenta_concrete","orange_concrete","pink_concrete","purple_concrete","red_concrete","light_gray_concrete","white_concrete","yellow_concrete","black_concrete_powder","blue_concrete_powder","brown_concrete_powder","cyan_concrete_powder","gray_concrete_powder","green_concrete_powder","light_blue_concrete_powder","lime_concrete_powder","magenta_concrete_powder","orange_concrete_powder","pink_concrete_powder","purple_concrete_powder","red_concrete_powder","light_gray_concrete_powder","white_concrete_powder","yellow_concrete_powder","black_glazed_terracotta","blue_glazed_terracotta","brown_glazed_terracotta","cyan_glazed_terracotta","gray_glazed_terracotta","green_glazed_terracotta","light_blue_glazed_terracotta","lime_glazed_terracotta","magenta_glazed_terracotta","orange_glazed_terracotta","pink_glazed_terracotta","purple_glazed_terracotta","red_glazed_terracotta","light_gray_glazed_terracotta","white_glazed_terracotta","yellow_glazed_terracotta","white_shulker_box","blank","water_overlay","tall_seagrass_top","tube_coral_block","bubble_coral_block","brain_coral_block","fire_coral_block","horn_coral_block","tube_coral","bubble_coral","brain_coral","fire_coral","horn_coral","sea_pickle","blue_ice","dried_kelp_top","dried_kelp_side","seagrass","tall_seagrass_bottom","dead_tube_coral_block","dead_bubble_coral_block","dead_brain_coral_block","dead_fire_coral_block","dead_horn_coral_block","tube_coral_fan","bubble_coral_fan","brain_coral_fan","fire_coral_fan","horn_coral_fan","blank","blank","large_kelp_bottom","large_kelp_bottom","large_kelp_bottom","large_kelp_bottom","large_kelp_top","large_kelp_top","large_kelp_top","large_kelp_top","seagrass_2","dead_tube_coral_fan","dead_bubble_coral_fan","dead_brain_coral_fan","dead_fire_coral_fan","dead_horn_coral_fan","blank","spruce_trapdoor","stripped_oak_log","stripped_oak_log_top","stripped_acacia_log","stripped_acacia_log_top","stripped_birch_log","stripped_birch_log_top","stripped_dark_oak_log","stripped_dark_oak_log_top","stripped_jungle_log","stripped_jungle_log_top","stripped_spruce_log","stripped_spruce_log_top","acacia_trapdoor","birch_trapdoor","dark_oak_trapdoor","jungle_trapdoor"]
            
            fires = ["fire_layer_0.png", "fire_layer_1.png"]
                
            if self.blocks_checkbox.isChecked():
                try:
                    os.makedirs(self.output_folder + "/fire")
                except FileExistsError:
                    pass
                except PermissionError:
                    pass
                for fire in fires:
                    file_path = os.path.join(self.input_folder + "/blocks/", fire)
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, self.output_folder + "/fire")
                        new_file_name = fire.replace("_layer", "")
                        new_file_path = os.path.join(self.output_folder + "/fire", new_file_name)
                        os.rename(os.path.join(self.output_folder + "/fire/", fire), new_file_path)
                        self.log_text_edit.append(f"{fire} copied and moved to : '/fire'")
                        
                    else:
                        if self.fallback_checkbox.isChecked():
                            file_path = os.path.join("fallback/fire/", fire)
                            if os.path.isfile(file_path):
                                shutil.copy(file_path, self.output_folder + "/fire")
                                new_file_name = fire.replace("_layer", "")
                                new_file_path = os.path.join(self.output_folder + "/fire", new_file_name)
                                os.rename(os.path.join(self.output_folder + "/fire", fire), new_file_path)
                                self.log_text_edit.append(f"{fire} copied and moved to : '/fire'")
                            else:
                                self.log_text_edit.append(f"{fire} not found ... Skipping")
                        else:
                            self.log_text_edit.append(f"{fire} not found ... Skipping")

            # create a new image with a transparent background
            blocks_image = Image.new("RGBA", (256, 544), (0, 0, 0, 0))
    
            # starting x and y coordinates for pasting images
            x = 0
            y = 0

            # iterate through the list of items
            # iterate through the list of items
            if self.blocks_checkbox.isChecked():
                for block in blocks:
                    # open the image file
                    try:
                        img = Image.open(self.input_folder + "/blocks/" + block + ".png")
                    except FileNotFoundError:
                        if self.fallback_checkbox.isChecked():
                            try:
                                img = Image.open("fallback/blocks/" + block + ".png")
                                self.log_text_edit.append(f"{block}.png not found ... using fallback")
                            except FileNotFoundError:
                                self.log_text_edit.append(f"{block}.png not found ... Skipped")
                                x += 16
                                continue
                        else:
                            self.log_text_edit.append(f"{block}.png not found ... Skipped")
                            x += 16
                            continue
                    # paste the image onto the new image
                    blocks_image.paste(img, (x, y))
                    self.log_text_edit.append(f"{block}.png pasted to : ({x}, {y})")
                    # increment x by 16 to move to the next square
                    x += 16
                    # if x is greater than or equal to 256, reset x to 0 and increment y by 16
                    if x >= 256:
                        x = 0
                        y += 16

                # save the new image
                blocks_image.save(os.path.join(self.output_folder, "terrain.png"))

                # resize the image to 128x272 and save it
                blocks_image_128 = blocks_image.resize((128, 272))
                blocks_image_128.save(os.path.join(self.output_folder, "terrainMipMapLevel2.png"))

                # resize the image to 64x136 and save it
                blocks_image_64 = blocks_image.resize((64, 136))
                blocks_image_64.save(os.path.join(self.output_folder, "terrainMipMapLevel3.png"))
                
        # function to convert the particles
        def convert_particles():
            # list of items to be placed on the image
            particles = ["particles"]

            # iterate through the list of items
            if self.particles_checkbox.isChecked():
                for particle in particles:
                    file_path = os.path.join(self.input_folder + "/particle/", particle + ".png")
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, self.output_folder)
                        self.log_text_edit.append(f"{particle}.png moved.")
                    else:
                        if self.fallback_checkbox.isChecked():
                            file_path = os.path.join("fallback/particle", particle + ".png")
                            if os.path.isfile(file_path):
                                shutil.copy(file_path, self.output_folder)
                                self.log_text_edit.append(f"{particle}.png moved.")
                            else:
                                self.log_text_edit.append(f"{particle}.png not found ... Skipping")
                        else:
                            self.log_text_edit.append(f"{particle}.png not found ... Skipping")
                            
        # function to convert the armor
        def convert_armor():
            # list of items to be placed on the image
            armors = ["chainmail_layer_1.png", "chainmail_layer_2.png", "diamond_layer_1.png", "diamond_layer_2.png", "gold_layer_1.png", "gold_layer_2.png", "iron_layer_1.png", "iron_layer_2.png"]
            leather_1 = ["leather_layer_1.png", "leather_layer_2.png"]
            leather_2 = ["leather_layer_1_overlay.png", "leather_layer_2_overlay.png"]
            

            
            # iterate through the list of items
            if self.armor_checkbox.isChecked():
                try:
                    os.makedirs(self.output_folder + "/armor")
                except FileExistsError:
                    pass
                for armor in armors:
                    file_path = os.path.join(self.input_folder + "/models/armor/", armor)
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, self.output_folder + "/armor")
                        new_file_name = armor.replace("_layer", "")
                        new_file_path = os.path.join(self.output_folder + "/armor", new_file_name)
                        os.rename(os.path.join(self.output_folder + "/armor/", armor), new_file_path)
                        self.log_text_edit.append(f"{armor} copied and moved to : '/armor'")
                        
                    else:
                        if self.fallback_checkbox.isChecked():
                            file_path = os.path.join("fallback/armor/", armor)
                            if os.path.isfile(file_path):
                                shutil.copy(file_path, self.output_folder + "/armor")
                                new_file_name = armor.replace("_layer", "")
                                new_file_path = os.path.join(self.output_folder + "/armor", new_file_name)
                                os.rename(os.path.join(self.output_folder + "/armor", armor), new_file_path)
                                self.log_text_edit.append(f"{armor} copied and moved to : '/armor'")
                            else:
                                self.log_text_edit.append(f"{armor} not found ... Skipping")
                        else:
                            self.log_text_edit.append(f"{armor} not found ... Skipping")
                            
            if self.armor_checkbox.isChecked():
                for leather in leather_1:
                    file_path = os.path.join(self.input_folder + "/models/armor/", leather)
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, self.output_folder + "/armor")
                        new_file_name = leather.replace("leather_layer", "cloth")
                        new_file_path = os.path.join(self.output_folder + "/armor", new_file_name)
                        os.rename(os.path.join(self.output_folder + "/armor/", leather), new_file_path)
                        self.log_text_edit.append(f"{leather} copied and moved to : '/armor'")
                    else:
                        if self.fallback_checkbox.isChecked():
                            file_path = os.path.join("fallback/armor/", leather)
                            if os.path.isfile(file_path):
                                shutil.copy(file_path, self.output_folder + "/armor")
                                new_file_name = leather.replace("leather_layer", "cloth")
                                new_file_path = os.path.join(self.output_folder + "/armor", new_file_name)
                                os.rename(os.path.join(self.output_folder + "/armor", leather), new_file_path)
                                self.log_text_edit.append(f"{leather} copied and moved to : '/armor'")
                            else:
                                self.log_text_edit.append(f"{leather} not found ... Skipping")
                        else:
                            self.log_text_edit.append(f"{leather} not found ... Skipping")
                            
            if self.armor_checkbox.isChecked():
                for leather in leather_2:
                    file_path = os.path.join(self.input_folder + "/models/armor/", leather)
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, self.output_folder + "/armor")
                        if leather == "leather_layer_1_overlay.png":
                             new_file_name = leather.replace("leather_layer_1_overlay", "cloth_1_b")
                        else:
                             new_file_name = leather.replace("leather_layer_2_overlay", "cloth_2_b")
                        new_file_path = os.path.join(self.output_folder + "/armor", new_file_name)
                        os.rename(os.path.join(self.output_folder + "/armor/", leather), new_file_path)
                        self.log_text_edit.append(f"{leather} copied and moved to : '/armor'")
                    else:
                        if self.fallback_checkbox.isChecked():
                            file_path = os.path.join("fallback/armor/", leather)
                            if os.path.isfile(file_path):
                                shutil.copy(file_path, self.output_folder + "/armor")
                                new_file_name = leather.replace("leather_layer", "cloth")
                                if leather == "leather_layer_1_overlay.png":
                                     new_file_name = leather.replace("leather_layer_1_overlay", "cloth_1_b")
                                else:
                                     new_file_name = leather.replace("leather_layer_2_overlay", "cloth_2_b")
                                new_file_path = os.path.join(self.output_folder + "/armor", new_file_name)
                                os.rename(os.path.join(self.output_folder + "/armor", leather), new_file_path)
                                self.log_text_edit.append(f"{leather} copied and moved to : '/armor'")
                            else:
                                self.log_text_edit.append(f"{leather} not found ... Skipping")
                        else:
                            self.log_text_edit.append(f"{leather} not found ... Skipping")
                            
        # function to convert the particles
        def convert_environment():
            # list of items to be placed on the image
            environments = ["clouds", "end_sky", "moon_phases", "rain", "snow", "sun"]

            # iterate through the list of items
            if self.environment_checkbox.isChecked():
                try:
                    os.makedirs(self.output_folder + "/environment")
                except FileExistsError:
                    pass
                for environment in environments:
                    file_path = os.path.join(self.input_folder + "/environment/", environment + ".png")
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, self.output_folder + "/environment")
                        self.log_text_edit.append(f"{environment}.png moved.")
                    else:
                        if self.fallback_checkbox.isChecked():
                            file_path = os.path.join("fallback/environment", environment + ".png")
                            if os.path.isfile(file_path):
                                shutil.copy(file_path, self.output_folder + "/environment")
                                self.log_text_edit.append(f"{environment}.png moved.")
                            else:
                                self.log_text_edit.append(f"{environment}.png not found ... Skipping")
                        else:
                            self.log_text_edit.append(f"{environment}.png not found ... Skipping")
                

        if not os.path.exists(self.output_folder):
            try:
                # Try to make / use designated Output folder
                os.makedirs(self.output_folder)
            # If operation fails, throw error
            except PermissionError as file_error:
                file_error_dialog = QtWidgets.QMessageBox()
                file_error_dialog.setWindowTitle('File Error!')
                file_error_dialog.setText(f"{file_error}\n\nSpecify an Output Path!")
                file_error_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.center_dialog(file_error_dialog)
                choice = file_error_dialog.exec_()
                var = 1
            except FileNotFoundError as file_error:
                file_error_dialog = QtWidgets.QMessageBox()
                file_error_dialog.setWindowTitle('File Error!')
                file_error_dialog.setText(f"{file_error}\n\nSpecify an Output Path!")
                file_error_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.center_dialog(file_error_dialog)
                choice = file_error_dialog.exec_()
                var = 1
        else:
            var = 0

        def full_start():
            convert_items()
            convert_blocks()
            convert_particles()
            convert_armor()
            convert_environment()

        # call the convert_items function
        if var == 0:
            full_start()
        else:
            pass

        # If Output dir is left empty, let FileError dialog show, but prevent Completion dialog from showing
        if self.output_folder == '':
            complete = False
        else:
            complete = True

        # Check whether or not Completion Dialog should show
        if complete == True:
            completion_dialog = QtWidgets.QMessageBox()
            completion_dialog.setWindowTitle('Process Complete!')
            completion_dialog.setText(f"Conversion process completed!")
            completion_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.center_dialog(completion_dialog)
            choice = completion_dialog.exec_()
        else:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
