from PIL import Image
import os

class ImageCreator:
    def __init__(self, directory, filenames, size, spacing=16, fallback_path=None):
        self.directory = directory
        self.filenames = filenames
        self.size = size
        self.spacing = spacing
        self.fallback_path = fallback_path

    def create_image(self):
        new_image = Image.new('RGBA', self.size, (0, 0, 0, 0))
        x, y = 0, 0
        for i, filename in enumerate(self.filenames):
            x = (i % 16) * self.spacing
            y = (i // 16) * self.spacing
            filepath = os.path.join(self.directory, filename)
            if not os.path.exists(filepath) and self.fallback_path is not None:
                filepath = os.path.join(self.fallback_path, filename)
            if not os.path.exists(filepath):
                continue
            with Image.open(filepath) as img:
                if img.size[0] > self.spacing or img.size[1] > self.spacing:
                    # Image is too big, use the fallback image instead
                    if self.fallback_path is not None:
                        fallback_filepath = os.path.join(self.fallback_path, filename)
                        if os.path.exists(fallback_filepath):
                            with Image.open(fallback_filepath) as fallback_img:
                                fallback_img = fallback_img.resize((self.spacing, self.spacing))
                                new_image.paste(fallback_img, (x, y))
                    continue
                img = img.resize((self.spacing, self.spacing))
                new_image.paste(img, (x, y))
        return new_image
