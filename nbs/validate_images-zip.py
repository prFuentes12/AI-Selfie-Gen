import mimetypes
import pathlib
import shutil
import tempfile

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()
NBS_DIR = pathlib.Path().resolve()
REPO_DIR = NBS_DIR.parent
DATA_DIR = REPO_DIR / "data"
INPUTS_DIR = DATA_DIR / "inputs"
READY_DIR = DATA_DIR / "ready"
OUTPUTS_DIR = DATA_DIR / "outputs"


def perform_is_image(path, require_can_open=True):
    try:
        guessed_type, encoding = mimetypes.guess_type(path)
    except:
        guessed_type = ""
    guessed_image = "image" in guessed_type
    if not guessed_image:
        return False
    if guessed_image and require_can_open:
        try:
            img_ = Image.open(path)
        except:
            return False
    return True

image_file_paths = []

for file_path in INPUTS_DIR.glob("*"):
    is_image = perform_is_image(file_path)
    if not is_image:
        continue
    image_file_paths.append(file_path)

OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)
zip_outpath = OUTPUTS_DIR / "images.zip"
zip_outpath.exists()

zip_outpath.with_suffix('')

with tempfile.TemporaryDirectory() as temp_dir:
    for path in image_file_paths:
        shutil.copy(path, temp_dir)
    shutil.make_archive(zip_outpath.with_suffix(''), 'zip', temp_dir)
