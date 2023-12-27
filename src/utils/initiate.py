from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import google.generativeai as palm
import os
from dotenv import load_dotenv

load_dotenv()


async def init_pipeline():
    model_name = "mrm8488/electra-small-finetuned-squadv2"
    nlp = pipeline("question-answering", model=model_name, max_length=1024, num_beans=5)
    return nlp


async def init_palm():
    palm.configure(api_key=os.environ.get("PALM_API_KEY"))
    models = [
        m
        for m in palm.list_models()
        if "generateText" in m.supported_generation_methods
    ]
    model = models[0].name
    return model
