import pathlib
from decouple import config
from replicate.client import Client

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
prompt = "a photo of TOK adult man dressed up for a sports photo shoot"
num_outputs = 2
output_format = "jpg"

input_args = {
    "prompt": prompt,
    "num_outputs": 2,
    "output_format": "jpg",
}

rep_model = replicate_client.models.get(REPLICATE_MODEL)
rep_version = rep_model.versions.get(REPLICATE_MODEL_VERSION)

pred = replicate_client.predictions.create(
    version=rep_version,
    input=input_args
)

pred_id = "dat0d05k01rma0ck9cn8hs27aw"
pred_lookup = replicate_client.predictions.get(pred_id)

pred_urls = pred_lookup.output


import httpx
import random

session_id = random.randint(1_000, 40_000)
with httpx.Client() as client:
    for i, url in enumerate(pred_urls):
        fname = f"{i}-{session_id}.jpg"
        outpath = GENERATED_DIR / fname
        res = client.get(url)
        res.raise_for_status()
        with open(outpath, 'wb') as f:
            f.write(res.content)