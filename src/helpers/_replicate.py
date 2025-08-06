from functools import lru_cache

from decouple import config
from replicate.client import Client

REPLICATE_API_TOKEN = config("REPLICATE_API_TOKEN")
REPLICATE_MODEL = config("REPLICATE_MODEL", default="codingforentrepreneurs/superme-justin-v1")
REPLICATE_MODEL_VERSION = config("REPLICATE_MODEL_VERSION", default="4bc2a39fa73d29cd531c57ad4f56bede13378ce3da2f6f517684b0b61bd192d7")



@lru_cache
def get_replicate_client():
    return  Client(api_token=REPLICATE_API_TOKEN)

@lru_cache
def get_replicate_model_version():
    replicate_client = get_replicate_client()
    rep_model = replicate_client.models.get(REPLICATE_MODEL)
    rep_version = rep_model.versions.get(REPLICATE_MODEL_VERSION)

    return rep_version

def generate_image(prompt):
    input_args = {
        "prompt": prompt,
        "num_outputs": 2,
        "output_format": "jpg",
    }

    replicate_client = get_replicate_client()
    rep_version = get_replicate_model_version()
    pred = replicate_client.predictions.create(
        version=rep_version,
        input=input_args
    )
    return {"pred": pred.id,
            "status" : pred.status}