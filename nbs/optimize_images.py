import mimetypes
import pathlib
import shutil
import tempfile

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

register_heif_opener()
NBS_DIR = pathlib.Path().resolve()
REPO_DIR = NBS_DIR.parent
DATA_DIR = REPO_DIR / "data"
INPUTS_DIR = DATA_DIR / "inputs"
READY_DIR = DATA_DIR / "ready"
OUTPUTS_DIR = DATA_DIR / "outputs"


def perform_clear_and_optimize_image(image_path, output_path, max_size=(1920, 1920)):
    """
    Removes all metadata from an image (e.g. EXIF data).
    Optimizes the image file size while preserving quality and transparency when needed.
    """
    # Convert to Path objects
    image_path = pathlib.Path(image_path)
    output_path = pathlib.Path(output_path)
    
    # Open and create clean copy
    original = Image.open(image_path)

    # Determine if image has transparency
    has_transparency = (
        original.mode in ('RGBA', 'LA') or 
        (original.mode == 'P' and 'transparency' in original.info)
    )
    
    # Auto-rotate based on EXIF
    original = ImageOps.exif_transpose(original)

    # Resize if larger than max_size while maintaining aspect ratio
    if original.size[0] > max_size[0] or original.size[1] > max_size[1]:
        original.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Convert mode based on transparency
    if has_transparency:
        if original.mode != 'RGBA':
            original = original.convert('RGBA')
        best_format = 'PNG'
    else:
        if original.mode in ('RGBA', 'P', 'LA'):
            original = original.convert('RGB')
        best_format = 'JPEG'

    # Save with optimized settings
    save_kwargs = {}
    if best_format == 'JPEG':
        save_kwargs.update({
            'quality': 85,
            'optimize': True,
            'progressive': True
        })
        output_path = output_path.with_suffix('.jpg')
    elif best_format == 'PNG':
        save_kwargs.update({
            'optimize': True,
            'compress_level': 6
        })
        output_path = output_path.with_suffix('.png')
    print(f'Saving {output_path}')
    original.save(output_path, format=best_format, **save_kwargs)
    return output_path


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
    start_output_path = READY_DIR / file_path.name
    final_output_path = perform_clear_and_optimize_image(file_path, start_output_path)
    image_file_paths.append(final_output_path)

OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)

zip_outpath = OUTPUTS_DIR / "images-optimized.zip"


with tempfile.TemporaryDirectory() as temp_dir:
    for path in image_file_paths:
        shutil.copy(path, temp_dir)
    shutil.make_archive(zip_outpath.with_suffix(''), 'zip', temp_dir)