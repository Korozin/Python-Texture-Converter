import shutil
import os

class FileMover:
    def __init__(self, source_dir, fallback_dir, output_dir, filename_map):
        self.source_dir = source_dir
        self.fallback_dir = fallback_dir
        self.output_dir = output_dir
        self.filename_map = filename_map

    def convert(self):
        for source_filename, output_filename in self.filename_map.items():
            source_filepath = os.path.join(self.source_dir, source_filename)
            if os.path.exists(source_filepath):
                if not os.path.exists(self.output_dir):
                    os.makedirs(self.output_dir)

                output_filepath = os.path.join(self.output_dir, output_filename)
                shutil.copy(source_filepath, output_filepath)
            elif self.fallback_dir is not None:
                fallback_filepath = os.path.join(self.fallback_dir, source_filename)
                if os.path.exists(fallback_filepath):
                    if not os.path.exists(self.output_dir):
                        os.makedirs(self.output_dir)

                    output_filepath = os.path.join(self.output_dir, output_filename)
                    shutil.copy(fallback_filepath, output_filepath)
