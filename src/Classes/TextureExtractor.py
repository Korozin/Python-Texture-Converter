import os
import zipfile


class TextureExtractor:
    def __init__(self, version, zip_path, output_path):
        self.version = version
        self.zip_path = zip_path
        self.output_path = output_path

    def extract_main(self, folder_path):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                member.filename = member.filename.replace("\\", "/")
                if member.filename.startswith(folder_path):
                    member.filename = os.path.relpath(member.filename, folder_path)
                    target_path = os.path.join(self.output_path, member.filename)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    if target_path.endswith(".png"):
                        open(target_path, 'wb').write(zip_ref.read(member))

    def extract_textures(self):
        if self.version == "1.8":
            __Path = 'assets/minecraft/textures/'
        elif self.version == "1.13+":
            # it can vary, but usually the same as 1.8
            # acts as placeholder for now until it needs
            # to be changed
            __Path = 'assets/minecraft/textures/'
        else:
            raise ValueError("Unsupported Version!")

        self.extract_main(__Path)
