
import pathlib
import random
from replicate.client import Client
from decouple import config

NBS_DIR = pathlib.Path().resolve()
REPO_DIR = NBS_DIR.parent
DATA_DIR = REPO_DIR / "data"
GENERATED_DIR = DATA_DIR / "generated"
GENERATED_DIR.mkdir(exist_ok=True, parents=True)


REPLICATE_API_TOKEN = config("REPLICATE_API_TOKEN")
REPLICATE_MODEL = config("REPLICATE_MODEL", default="codingforentrepreneurs/superme-justin-v1")
REPLICATE_MODEL_VERSION = config("REPLICATE_MODEL_VERSION", default="4bc2a39fa73d29cd531c57ad4f56bede13378ce3da2f6f517684b0b61bd192d7")


replicate_client = Client(api_token=REPLICATE_API_TOKEN)

model = f"{REPLICATE_MODEL}:{REPLICATE_MODEL_VERSION}"
prompt = "a photo of TOK adult man dressed up for a professional photo shoot"

responses = replicate_client.run(
    model,
    input={
        "model": "dev",
        "prompt": prompt,
        "num_outputs": 4,
        "output_format": "jpg",
    }
)
print(responses)

len(responses)

session_id = random.randint(1_000, 40_000)
for i, output in enumerate(responses):
    fname = f"{i}-{session_id}.jpg"
    outpath = GENERATED_DIR / fname
    with open(outpath, 'wb') as f:
        f.write(output.read())