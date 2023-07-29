import os
import zipfile

class TextureExtractor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        
    def extract_textures(self):
        with zipfile.ZipFile(self.input_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                if 'textures' in name and name.endswith('/'):
                    textures_path = os.path.dirname(name)
                    for member in zip_ref.infolist():
                        if member.filename.startswith(textures_path) and not member.is_dir():
                            member.filename = os.path.relpath(member.filename, textures_path)
                            target_path = os.path.join(self.output_path, member.filename)
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            with open(target_path, 'wb') as target:
                                target.write(zip_ref.read(member))
                    return True
        return False
