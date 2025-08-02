import pathlib
import mimetypes
import shutil
import tempfile 

NBS_DIR= pathlib.Path(__file__).parent
REPO_DIR = NBS_DIR.parent
DATA_DIR = REPO_DIR / "data"
INPUTS_DIR = DATA_DIR / "inputs"
OUTPUTS_DIR = DATA_DIR / "outputs"


images_files_path = []

for file_path in INPUTS_DIR.glob("*") :
    guessed_type, encoding = mimetypes.guess_type(file_path)
    if ("image" not in guessed_type):
        continue
    else :
        images_files_path.append(file_path)


OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)
