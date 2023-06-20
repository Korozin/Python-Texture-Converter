import os, sys, shutil, argparse, requests
from zipfile import ZipFile
from PIL import Image

# Terminal Colors
red = '\033[91m'
dred = '\033[31m'
yellow = '\033[93m'
green = '\033[92m'
clear = '\033[0m'
cyan = '\033[96m'
magenta = '\033[95m'
default = '\033[97m'

def convert_items():

    # create output folder if it doesn't exist
    if not os.path.exists('output'):
        os.mkdir('output')

    # create a new transparent image with size 256x272
    items = Image.new('RGBA', (256, 272), (0, 0, 0, 0))

    # list of image filenames to paste onto the new image
    items_filenames = ["leather_helmet","chainmail_helmet","iron_helmet","diamond_helmet","gold_helmet","flint_and_steel","flint","coal","string","seeds_wheat","apple","apple_golden","egg","sugar","snowball","elytra","leather_chestplate","chainmail_chestplate","iron_chestplate","diamond_chestplate","gold_chestplate","bow_standby","brick","iron_ingot","feather","wheat","painting","sugarcane","bone","cake","slimeball","broken_elytra","leather_leggings","chainmail_leggings","iron_leggings","diamond_leggings","gold_leggings","arrow","end_crystal","gold_ingot","gunpowder","bread","sign","door_wood","door_iron","blank","fireball","chorus_fruit","leather_boots","chainmail_boots","iron_boots","diamond_boots","gold_boots","stick","compass_00","diamond","redstone_dust","clay_ball","paper","book_normal","map_empty","seeds_pumpkin","seeds_melon","popped_chorus_fruit","wood_sword","stone_sword","iron_sword","diamond_sword","gold_sword","fishing_rod_uncast","clock_00","bowl","mushroom_stew","glowstone_dust","bucket_empty","bucket_water","bucket_lava","bucket_milk","dye_powder_black","dye_powder_gray","wood_shovel","stone_shovel","iron_shovel","diamond_shovel","gold_shovel","fishing_rod_cast","repeater","porkchop_raw","porkchop_cooked","fish_cod_raw","fish_cod_cooked","rotten_flesh","cookie","shears","dye_powder_red","dye_powder_pink","wood_pickaxe","stone_pickaxe","iron_pickaxe","diamond_pickaxe","gold_pickaxe","bow_pulling_0","carrot_on_a_stick","leather","saddle","beef_raw","beef_cooked","ender_pearl","blaze_rod","melon","dye_powder_green","dye_powder_lime","wood_axe","stone_axe","iron_axe","diamond_axe","gold_axe","bow_pulling_1","potato_baked","potato","carrot","chicken_raw","chicken_cooked","ghast_tear","gold_nugget","nether_wart","dye_powder_brown","dye_powder_yellow","wood_hoe","stone_hoe","iron_hoe","diamond_hoe","gold_hoe","bow_pulling_2","potato_poisonous","minecart_normal","boat","melon_speckled","spider_eye_fermented","spider_eye","potion_bottle_drinkable","potion_overlay","dye_powder_blue","dye_powder_light_blue","leather_helmet_overlay","spectral_arrow","iron_horse_armor","diamond_horse_armor","gold_horse_armor","comparator","carrot_golden","minecart_chest","pumpkin_pie","spawn_egg","potion_bottle_splash","ender_eye","cauldron","blaze_powder","dye_powder_purple","dye_powder_magenta","blank","tipped_arrow_base","dragon_breath","name_tag","lead","netherbrick","fish_clownfish_raw","minecart_furnace","charcoal","spawn_egg_overlay","blank","experience_bottle","brewing_stand","magma_cream","dye_powder_cyan","dye_powder_orange","leather_leggings_overlay","tipped_arrow_head","lingering_potion","barrier","mutton_raw","rabbit_raw","fish_pufferfish_raw","minecart_hopper","hopper","nether_star","emerald","book_writable","book_written","flower_pot","dye_powder_silver","dye_powder_white","leather_boots_overlay","beetroot","beetroot_seeds","beetroot_soup","mutton_cooked","rabbit_cooked","fish_salmon_raw","minecart_tnt","armor_stand","fireworks","fireworks_charge","fireworks_charge_overlay","quartz","map","item_frame","book_enchanted","door_acacia","door_birch","door_dark_oak","door_jungle","door_spruce","rabbit_stew","fish_salmon_cooked","minecart_command_block","acacia_boat","birch_boat","dark_oak_boat","jungle_boat","spruce_boat","prismarine_shard","prismarine_crystals","leather_horse_armor","structure_void","blank","totem_of_undying","shulker_shell","iron_nugget","rabbit_foot","rabbit_hide","blank","blank","blank","blank","blank","blank","blank","blank","dragon_charge","13","cat","blocks","chirp","far","mall","mellohi","stal","strad","ward","11","wait","cod_bucket","salmon_bucket","pufferfish_bucket","tropical_fish_bucket","leather_horse_overlay","blank","blank","blank","blank","blank","blank","kelp","dried_kelp","sea_pickle","nautilus_shell","heart_of_the_sea","turtle_helmet","scute","trident","phantom_membrane"]

    # iterate through the list of image filenames and paste them onto the new image
    for i, filename in enumerate(items_filenames):
        x = (i % 16) * 16
        y = (i // 16) * 16
        try:
            img = Image.open(f'tmp/assets/minecraft/textures/items/{filename}.png')
            items.paste(img, (x, y))
            print(f"{magenta}[normal]:{default} {green}{filename}.png{default} pasted to: {yellow}({x}, {y})")
        except FileNotFoundError:
            try:
                img = Image.open(f'fallback/items/{filename}.png')
                items.paste(img, (x, y))
                print(f"{cyan}[fallback]:{default} {green}{filename}.png{default} pasted to: {yellow}({x}, {y})")
                continue
            except FileNotFoundError:
                print(f"{dred}[skipped]:{default} {green}{filename}.png{default} not found ... {red}Skipping")
                continue
    
    # save the new image to the output folder
    items.save('output/items.png')
    
def convert_blocks():

    # create output folder if it doesn't exist
    if not os.path.exists('output'):
        os.mkdir('output')

    # create a new transparent image with size 256x272
    terrain = Image.new('RGBA', (256, 544), (0, 0, 0, 0))

    # list of image filenames to paste onto the new image
    terrain_filenames = ["grass_top","stone","dirt","grass_side","planks_oak","stone_slab_side","stone_slab_top","brick","tnt_side","tnt_top","tnt_bottom","web","poppy","flower_dandelion","blue_concrete","sapling_oak","cobblestone","bedrock","sand","gravel","log_oak","log_oak_top","iron_block","gold_block","diamond_block","emerald_block","redstone_block","dropper_front_horizontal","mushroom_red","mushroom_brown","sapling_jungle","red_concrete","gold_ore","iron_ore","coal_ore","bookshelf","cobblestone_mossy","obsidian","grass_side_overlay","tallgrass","dispenser_front_vertical","beacon","dropper_front_vertical","crafting_table_top","furnace_front_off","furnace_side","dispenser_front_horizontal","red_concrete","sponge","glass","diamond_ore","redstone_ore","leaves_oak","black_concrete","stonebrick","dead_bush","fern","daylight_detector_top","daylight_detector_side","crafting_table_side","crafting_table_front","furnace_front_on","furnace_top","sapling_spruce","wool_colored_white","mob_spawner","snow","ice","snow","cactus_top","cactus_side","cactus_bottom","clay","reeds","jukebox_side","jukebox_top","leaves_birch","mycelium_side","mycelium_top","sapling_birch","torch_on","door_wood_upper","door_iron_upper","ladder","trapdoor","iron_bars","farmland_wet","farmland_dry","wheat_stage_0","wheat_stage_1","wheat_stage_2","wheat_stage_3","wheat_stage_4","wheat_stage_5","wheat_stage_6","wheat_stage_7","lever","door_wood_lower","door_iron_lower","redstone_torch_on","stonebrick_mossy","stonebrick_cracked","pumpkin_top","netherrack","soul_sand","glowstone","piston_top_sticky","piston_top","piston_side","piston_bottom","piston_inner","pumpkin_stem_disconnected","rail_normal_turned","wool_colored_black","wool_colored_gray","redstone_torch_off","spruce_log","log_birch","pumpkin_side","pumpkin_face_off","pumpkin_face_on","cake_top","cake_side","cake_inner","cake_bottom","mushroom_block_skin_red","mushroom_block_skin_red","pumpkin_stem_connected","rail_normal","wool_colored_red","wool_colored_pink","repeater_off","leaves_spruce","leaves_spruce","conduit","turtle_egg","melon_side","melon_top","cauldron_top","cauldron_inner","sponge_wet","mushroom_block_skin_stem","mushroom_block_inside","vine","lapis_block","wool_colored_green","wool_colored_lime","repeater_on","glass_pane_top","chest_top","ender_chest_top","turtle_egg_slightly_cracked","turtle_egg_very_cracked","jungle_log","cauldron_side","cauldron_bottom","brewing_stand_base","brewing_stand","endframe_top","endframe_side","lapis_ore","wool_colored_brown","wool_colored_yellow","rail_golden","redstone_cross","redstone_line_horizontal","enchanting_table_top","dragon_egg","cocoa_stage_2","cocoa_stage_1","cocoa_stage_0","emerald_ore","trip_wire_source","trip_wire","end_portal_frame_eye","end_stone","sandstone_top","wool_colored_blue","wool_colored_light_blue","rail_golden_powered","blank","blank","enchanting_table_side","enchanting_table_bottom","glide_blue","item_frame","flower_pot","comparator_off","comparator_on","rail_activator","rail_activator_powered","quartz_ore","sandstone_normal","wool_colored_purple","wool_colored_magenta","rail_detector","jungle_leaves","black_concrete","planks_spruce","planks_jungle","carrots_stage_0","carrots_stage_1","carrots_stage_2","carrots_stage_3","slime","water_debug","water_debug","water_debug","sandstone_bottom","wool_colored_cyan","wool_colored_orange","redstone_lamp_off","redstone_lamp_on","stonebrick_carved","planks_birch","anvil_base","anvil_top_damaged_1","quartz_block_chiseled_top","quartz_block_lines_top","quartz_block_side","hopper_outside","rail_detector_powered","water_debug","water_debug","nether_brick","wool_colored_silver","nether_wart_stage_0","nether_wart_stage_1","nether_wart_stage_2","sandstone_carved","sandstone_smooth","anvil_top_damaged_0","anvil_top_damaged_2","chiseled_quartz_block_bottom","quartz_block_lines","quartz_block_top","hopper_inside","lava_debug","lava_debug","lava_debug","destroy_stage_0","destroy_stage_1","destroy_stage_2","destroy_stage_3","destroy_stage_4","destroy_stage_5","destroy_stage_6","destroy_stage_7","destroy_stage_8","destroy_stage_9","hay_block_side","quartz_block_bottom","hopper_top","hay_block_top","lava_debug","lava_debug","coal_block","hardened_clay","noteblock","stone_andesite","stone_andesite_smooth","stone_diorite","stone_diorite_smooth","stone_granite","stone_granite_smooth","potatoes_stage_0","potatoes_stage_1","potatoes_stage_2","potatoes_stage_3","log_spruce_top","log_jungle_top","log_birch_top","hardened_clay_stained_black","hardened_clay_stained_blue","hardened_clay_stained_brown","hardened_clay_stained_cyan","hardened_clay_stained_gray","hardened_clay_stained_green","hardened_clay_stained_light_blue","hardened_clay_stained_lime","hardened_clay_stained_magenta","hardened_clay_stained_orange","hardened_clay_stained_pink","hardened_clay_stained_purple","hardened_clay_stained_red","hardened_clay_stained_silver","hardened_clay_stained_white","hardened_clay_stained_yellow","glass_black","glass_blue","glass_brown","glass_cyan","glass_gray","glass_green","glass_light_blue","glass_lime","glass_magenta","glass_orange","glass_pink","glass_purple","glass_red","glass_silver","glass_white","glass_yellow","glass_pane_top_black","glass_pane_top_blue","glass_pane_top_brown","glass_pane_top_cyan","glass_pane_top_gray","glass_pane_top_green","glass_pane_top_light_blue","glass_pane_top_lime","glass_pane_top_magenta","glass_pane_top_orange","glass_pane_top_pink","glass_pane_top_purple","glass_pane_top_red","glass_pane_top_silver","glass_pane_top_white","glass_pane_top_yellow","double_plant_fern_top","double_plant_grass_top","double_plant_paeonia_top","double_plant_rose_top","double_plant_syringa_top","flower_tulip_orange","double_plant_sunflower_top","double_plant_sunflower_front","acacia_log","acacia_log_top","planks_acacia","leaves_acacia","leaves_acacia","prismarine_bricks","red_sand","red_sandstone_top","double_plant_fern_bottom","double_plant_grass_bottom","double_plant_paeonia_bottom","double_plant_rose_bottom","double_plant_syringa_bottom","flower_tulip_pink","double_plant_sunflower_bottom","double_plant_sunflower_bottom","dark_oak_log","dark_oak_log_top","planks_big_oak","leaves_big_oak","leaves_big_oak","dark_prismarine","red_sandstone_bottom","red_sandstone_normal","flower_allium","flower_blue_orchid","flower_houstonia","flower_oxeye_daisy","flower_tulip_red","flower_tulip_white","sapling_acacia","sapling_roofed_oak","coarse_dirt","dirt_podzol_side","dirt_podzol_top","leaves_spruce","leaves_spruce","rough_prismarine","red_sandstone_carved","red_sandstone_smooth","door_acacia_upper","door_birch_upper","door_dark_oak_upper","door_jungle_upper","door_spruce_upper","chorus_flower","chorus_flower_dead","chorus_plant","end_stone_bricks","grass_path_side","grass_path_top","barrier","ice_packed","sea_lantern","daylight_detector_inverted_top","iron_trapdoor","door_acacia_lower","door_birch_lower","door_dark_oak_lower","door_jungle_lower","door_spruce_lower","purpur_block","purpur_pillar","purpur_pillar_top","end_rod","magma","nether_wart_block","red_nether_bricks","frosted_ice_0","frosted_ice_1","frosted_ice_2","frosted_ice_3","beetroots_stage_0","beetroots_stage_1","beetroots_stage_2","beetroots_stage_3","green_cmd","green_cmd","green_cmd","green_cmd","cmd","cmd","cmd","cmd","purple_cmd","purple_cmd","purple_cmd","purple_cmd","bone_block_side","bone_block_top","melon_stem_disconnected","melon_stem_connected","observer_front","observer_side","observer_back","observer_back_on","observer_top","glide_yellow","glide_green","structure_block","structure_block_corner","structure_block_data","structure_block_load","structure_block_save","black_concrete","blue_concrete","brown_concrete","cyan_concrete","gray_concrete","green_concrete","light_blue_concrete","lime_concrete","magenta_concrete","orange_concrete","pink_concrete","purple_concrete","red_concrete","light_gray_concrete","white_concrete","yellow_concrete","black_concrete_powder","blue_concrete_powder","brown_concrete_powder","cyan_concrete_powder","gray_concrete_powder","green_concrete_powder","light_blue_concrete_powder","lime_concrete_powder","magenta_concrete_powder","orange_concrete_powder","pink_concrete_powder","purple_concrete_powder","red_concrete_powder","light_gray_concrete_powder","white_concrete_powder","yellow_concrete_powder","black_glazed_terracotta","blue_glazed_terracotta","brown_glazed_terracotta","cyan_glazed_terracotta","gray_glazed_terracotta","green_glazed_terracotta","light_blue_glazed_terracotta","lime_glazed_terracotta","magenta_glazed_terracotta","orange_glazed_terracotta","pink_glazed_terracotta","purple_glazed_terracotta","red_glazed_terracotta","light_gray_glazed_terracotta","white_glazed_terracotta","yellow_glazed_terracotta","white_shulker_box","blank","water_overlay","tall_seagrass_top","tube_coral_block","bubble_coral_block","brain_coral_block","fire_coral_block","horn_coral_block","tube_coral","bubble_coral","brain_coral","fire_coral","horn_coral","sea_pickle","blue_ice","dried_kelp_top","dried_kelp_side","seagrass","tall_seagrass_bottom","dead_tube_coral_block","dead_bubble_coral_block","dead_brain_coral_block","dead_fire_coral_block","dead_horn_coral_block","tube_coral_fan","bubble_coral_fan","brain_coral_fan","fire_coral_fan","horn_coral_fan","blank","blank","large_kelp_bottom","large_kelp_bottom","large_kelp_bottom","large_kelp_bottom","large_kelp_top","large_kelp_top","large_kelp_top","large_kelp_top","seagrass_2","dead_tube_coral_fan","dead_bubble_coral_fan","dead_brain_coral_fan","dead_fire_coral_fan","dead_horn_coral_fan","blank","spruce_trapdoor","stripped_oak_log","stripped_oak_log_top","stripped_acacia_log","stripped_acacia_log_top","stripped_birch_log","stripped_birch_log_top","stripped_dark_oak_log","stripped_dark_oak_log_top","stripped_jungle_log","stripped_jungle_log_top","stripped_spruce_log","stripped_spruce_log_top","acacia_trapdoor","birch_trapdoor","dark_oak_trapdoor","jungle_trapdoor"]

    # iterate through the list of image filenames and paste them onto the new image
    for i, filename in enumerate(terrain_filenames):
        x = (i % 16) * 16
        y = (i // 16) * 16
        try:
            img = Image.open(f'tmp/assets/minecraft/textures/blocks/{filename}.png')
            terrain.paste(img, (x, y))
            print(f"{magenta}[normal]:{default} {green}{filename}.png{default} pasted to: {yellow}({x}, {y})")
        except FileNotFoundError:
            try:
                img = Image.open(f'fallback/blocks/{filename}.png')
                terrain.paste(img, (x, y))
                print(f"{cyan}[fallback]:{default} {green}{filename}.png{default} pasted to: {yellow}({x}, {y})")
                continue
            except FileNotFoundError:
                print(f"{dred}[skipped]:{default} {green}{filename}.png{default} not found ... {red}Skipping")
                continue
    
    # save the new image to the output folder
    terrain.save('output/terrain.png')
    
    # resize image and save
    mipMapLevel2 = terrain.resize((128, 272))
    mipMapLevel2.save('output/terrainMipMapLevel2.png')
    
    # resize image and save
    mipMapLevel3 = terrain.resize((64, 136))
    mipMapLevel3.save('output/terrainMipMapLevel3.png')
    
def convert_armor():

    # create output folder if it doesn't exist
    if not os.path.exists('output/armor'):
        os.mkdir('output/armor')

    source_dir = 'tmp/assets/minecraft/textures/models/armor'
    fallback_dir = 'fallback/armor'
    output_dir = 'output/armor'
    
    filename_map = {
        'chainmail_layer_1': 'chain_1',
        'chainmail_layer_2': 'chain_2',
        'diamond_layer_1': 'diamond_1',
        'diamond_layer_2': 'diamond_2',
        'gold_layer_1': 'gold_1',
        'gold_layer_2': 'gold_2',
        'iron_layer_1': 'iron_1',
        'iron_layer_2': 'iron_2',
        'leather_layer_1': 'cloth_1',
        'leather_layer_2': 'cloth_2',
        'leather_layer_1_overlay': 'cloth_1_b',
        'leather_layer_2_overlay': 'cloth_2_b'
    }

    # Iterate over the filename map
    for source_filename, output_filename in filename_map.items():
        # Check if the file exists in the source directory
        source_filepath = os.path.join(source_dir, source_filename + '.png')
        if os.path.exists(source_filepath):
            # File exists in the source directory, copy it to the output directory
            output_filepath = os.path.join(output_dir, output_filename + '.png')
            shutil.copy(source_filepath, output_filepath)
            print(f"{magenta}[normal]:{default} {green}{source_filename}.png{default} moved to: {yellow}/armor/{output_filename}.png")
        else:
            # File doesn't exist in the source directory, check the fallback directory
            fallback_filepath = os.path.join(fallback_dir, source_filename + '.png')
            if os.path.exists(fallback_filepath):
                # File exists in the fallback directory, copy it to the output directory
                output_filepath = os.path.join(output_dir, output_filename + '.png')
                shutil.copy(fallback_filepath, output_filepath)
                print(f"{cyan}[fallback]:{default} {green}{source_filename}.png{default} moved to: {yellow}/armor/{output_filename}.png")
            else:
                # File doesn't exist in either directory, print an error message
                print(f"{dred}[skipped]:{default} {green}{source_filename}.png{default} not found ... {red}Skipping")
    
def convert_environment():

    # create output folder if it doesn't exist
    if not os.path.exists("output/environment"):
        os.makedirs('output/environment')

    if not os.path.exists("output/terrain"):
        os.makedirs('output/terrain')

    # List of filenames to search for in the input folder
    filenames = ['clouds', 'end_sky', 'moon_phases', 'rain', 'snow', 'sun']

    # Loop through the filenames
    for filename in filenames:
        # Create the source path by appending the filename to the input folder path
        source_path = os.path.join('tmp/assets/minecraft/textures/environment', filename + '.png')
        # Check if the file exists in the input folder
        if os.path.exists(source_path):
            # Create the destination folder path based on the filename
            if filename in ['clouds', 'rain', 'snow']:
                dest_path = os.path.join('output', 'environment', filename + '.png')
            else:
                dest_path = os.path.join('output', 'terrain', filename + '.png')
            # Copy the file from the source path to the destination path
            shutil.copyfile(source_path, dest_path)
            print(f"{magenta}[normal]:{default} {green}{filename}.png{default} moved to: {yellow}/{dest_path}")
        else:
            # If the file doesn't exist in the input folder, search the fallback folder
            fallback_path = os.path.join('fallback', 'environment', filename + '.png')
            if os.path.exists(fallback_path):
                # Create the destination folder path based on the filename
                if filename in ['clouds', 'rain', 'snow']:
                    dest_path = os.path.join('output', 'environment', filename + '.png')
                else:
                    dest_path = os.path.join('output', 'terrain', filename + '.png')
                # Copy the file from the fallback folder to the destination path
                shutil.copyfile(fallback_path, dest_path)
                print(f"{cyan}[fallback]:{default} {green}{filename}.png{default} moved to: {yellow}/{dest_path}")
            else:
                print(f"{dred}[skipped]:{default} {green}{filename}.png{default} not found ... {red}Skipping")

    
def convert_particles():

    # create output folder if it doesn't exist
    if not os.path.exists('output'):
        os.mkdir('output')

    # Set the paths for the input and fallback folders
    input_folder = 'tmp/assets/minecraft/textures/particle'
    fallback_folder = 'fallback/particle'
    output_folder = 'output'

    # Set the filename to search for
    filename = 'particles.png'

    # Get the full path to the input file
    input_file_path = os.path.join(input_folder, filename)

    # Check if the input file exists
    if os.path.exists(input_file_path):
        # Get the full path to the output file
        output_file_path = os.path.join(output_folder, filename)

        # Copy the input file to the output folder
        shutil.copyfile(input_file_path, output_file_path)

        # Print a message indicating that the file was copied
        print(f"{magenta}[normal]:{default} {green}{filename}{default} moved to: {yellow}/{output_folder}")
    else:
        # Get the full path to the fallback file
        fallback_file_path = os.path.join(fallback_folder, filename)

        # Check if the fallback file exists
        if os.path.exists(fallback_file_path):
            # Get the full path to the output file
            output_file_path = os.path.join(output_folder, filename)

            # Copy the fallback file to the output folder
            shutil.copyfile(fallback_file_path, output_file_path)

            # Print a message indicating that the fallback file was copied
            print(f"{cyan}[fallback]:{default} {green}{filename}{default} moved to: {yellow}/{output_folder}")
        else:
            # Print an error message if the file doesn't exist in either folder
            print(f"{dred}[skipped]:{default} {green}{filename}{default} not found ... {red}Skipping")

def convert_fire():

    # create output folder if it doesn't exist
    if not os.path.exists('output/fire'):
        os.mkdir('output/fire')

    source_dir = 'tmp/assets/minecraft/textures/blocks'
    fallback_dir = 'fallback/fire'
    output_dir = 'output/fire'
    
    filename_map = {
        'fire_layer_0': 'fire_0',
        'fire_layer_1': 'fire_1',
    }

    # Iterate over the filename map
    for source_filename, output_filename in filename_map.items():
        # Check if the file exists in the source directory
        source_filepath = os.path.join(source_dir, source_filename + '.png')
        if os.path.exists(source_filepath):
            # File exists in the source directory, copy it to the output directory
            output_filepath = os.path.join(output_dir, output_filename + '.png')
            shutil.copy(source_filepath, output_filepath)
            print(f"{magenta}[normal]:{default} {green}{source_filename}.png{default} moved to: {yellow}/{output_dir}/{output_filename}.png")
        else:
            # File doesn't exist in the source directory, check the fallback directory
            fallback_filepath = os.path.join(fallback_dir, source_filename + '.png')
            if os.path.exists(fallback_filepath):
                # File exists in the fallback directory, copy it to the output directory
                output_filepath = os.path.join(output_dir, output_filename + '.png')
                shutil.copy(fallback_filepath, output_filepath)
                print(f"{cyan}[fallback]:{default} {green}{source_filename}.png{default} moved to: {yellow}/{output_dir}/{output_filename}.png")
            else:
                # File doesn't exist in either directory, print an error message
                print(f"{dred}[skipped]:{default} {green}{source_filename}.png{default} not found ... {red}Skipping")

def convert_misc():

    # create output folder if it doesn't exist
    if not os.path.exists('output/misc'):
        os.mkdir('output/misc')

    # Set the paths for the input and fallback folders
    input_folder = 'tmp/assets/minecraft/textures/misc'
    fallback_folder = 'fallback/misc'
    output_folder = 'output/misc'

    # Set the filenames to search for
    filenames = ['enchanted_item_glint', 'pumpkinblur', 'shadow']
    new_filenames = ['glint', 'pumpkinblur', 'shadow']  # New filenames to use for 'enchanted_item_glint'

    # Loop through the filenames
    for i, filename in enumerate(filenames):
        # Get the full path to the input file
        input_file_path = os.path.join(input_folder, filename + '.png')

        # Check if the input file exists
        if os.path.exists(input_file_path):
            # If the filename is 'enchanted_item_glint', use the new filename
            if filename == 'enchanted_item_glint':
                output_filename = new_filenames[i]
            else:
                output_filename = filename

            # Get the full path to the output file
            output_file_path = os.path.join(output_folder, output_filename + '.png')

            # Copy the input file to the output folder
            shutil.copyfile(input_file_path, output_file_path)

            # Print a message indicating that the file was copied
            print(f"{magenta}[normal]:{default} {green}{filename}.png{default} moved to: {yellow}/{output_folder}/{output_filename}.png")
        else:
            # Get the full path to the fallback file
            fallback_file_path = os.path.join(fallback_folder, filename + '.png')

            # Check if the fallback file exists
            if os.path.exists(fallback_file_path):
                # If the filename is 'enchanted_item_glint', use the new filename
                if filename == 'enchanted_item_glint':
                    output_filename = new_filenames[i]
                else:
                    output_filename = filename

                # Get the full path to the output file
                output_file_path = os.path.join(output_folder, output_filename + '.png')

                # Copy the fallback file to the output folder
                shutil.copyfile(fallback_file_path, output_file_path)

                # Print a message indicating that the fallback file was copied
                print(f"{cyan}[fallback]:{default} {green}{filename}.png{default} moved to: {yellow}/{output_folder}/{output_filename}.png")
            else:
                # Print an error message if the file doesn't exist in either folder
                print(f"{dred}[skipped]:{default} {green}{filename}.png{default} not found ... {red}Skipping")

    
def prepare_tmp(zip_file_name):
    # create tmp folder if it doesn't exist
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    # unzip the zip file into the tmp folder
    with ZipFile(zip_file_name, 'r') as zip:
        zip.extractall('tmp')

def set_args():
    parser = argparse.ArgumentParser(description="Convert 1.8 Texture Packs to Legacy Console")
    parser.add_argument("-items", "--convert_items", metavar="<zip path>", help="Converts only items")
    parser.add_argument("-blocks", "--convert_blocks", metavar="<zip path>", help="Converts only blocks")
    parser.add_argument("-armor", "--convert_armor", metavar="<zip path>", help="Converts only armor")
    parser.add_argument("-environment", "--convert_environment", metavar="<zip path>", help="Converts only environment / terrain")
    parser.add_argument("-particles", "--convert_particles", metavar="<zip path>", help="Converts only particles")
    parser.add_argument("-fire", "--convert_fire", metavar="<zip path>", help="Converts only fire")
    parser.add_argument("-misc", "--convert_misc", metavar="<zip path>", help="Converts only misc items")
    parser.add_argument("-all", "--convert_all", metavar="<zip path>", help="Converts everything")
    args = parser.parse_args()

    if args.convert_items:
        prepare_tmp(args.convert_items)
        convert_items()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    elif args.convert_blocks:
        prepare_tmp(args.convert_blocks)
        convert_blocks()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    elif args.convert_armor:
        prepare_tmp(args.convert_armor)
        convert_armor()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    elif args.convert_environment:
        prepare_tmp(args.convert_environment)
        convert_environment()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    elif args.convert_particles:
        prepare_tmp(args.convert_particles)
        convert_particles()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    elif args.convert_fire:
        prepare_tmp(args.convert_fire)
        convert_fire()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    elif args.convert_misc:
        prepare_tmp(args.convert_misc)
        convert_misc()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    elif args.convert_all:
        prepare_tmp(args.convert_all)
        convert_items()
        convert_blocks()
        convert_armor()
        convert_environment()
        convert_particles()
        convert_fire()
        convert_misc()
        shutil.rmtree('tmp')
        print(f"{yellow}[completion]:{default} Process Completed!{red} <3")
    else:
        parser.print_help()
        
def check_fallback():
    if not os.path.exists("fallback"):
        if os.path.exists("fallback.zip"):
            with ZipFile("fallback.zip", "r") as zip_ref:
                zip_ref.extractall("fallback")
            os.remove('fallback.zip')
        else:
            url = "https://korozin.github.io/assets/downloads/textures/fallback.zip"
            response = requests.get(url)
            open("fallback.zip", "wb").write(response.content)
            with ZipFile("fallback.zip", "r") as zip_ref:
                zip_ref.extractall("fallback")
            os.remove('fallback.zip')

if __name__ == "__main__":
    check_fallback()
    set_args()
