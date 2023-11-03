import os
import re
import json
import time
import nltk
import random
import pandas as pd
from pypdf import PdfReader

class NER:
    
    def __init__(self,FEWSHOT=0,CONSISTENCY_COUNT=0):
        self.few_shot = FEWSHOT
        self.consistency_count = CONSISTENCY_COUNT

    def retrieve_guideline(self):
        new_pages = []
        pdf_loader = PdfReader("./guideline/Annotation Guideline v3.pdf")
        pages = pdf_loader.pages
        for item in pages:
            p = item.extract_text().replace("\n"," ")
            nltk_tokens = nltk.word_tokenize(p)
            if len(nltk_tokens) < 4000:
                new_pages.append(" ".join(nltk_tokens))
            else:
                counter = floor(log(len(nltk_tokens))/log(4000))
                i = 0
                j = 0
                for item in range(counter):
                    j = i+4000
                    new_pages.append(" ".join(nltk_tokens[i:j]))
                    i = i+4000
                new_pages.append(" ".join(nltk_tokens[j:]))
        return(new_pages)

    def few_shot_with_explainations(self):
        with open("../informative_samples/entity/entities-with-explaination.json","r") as f:
            few_shot_samples = json.load(f)
        few_shot_samples = few_shot_samples[:self.few_shot]
        return(few_shot_samples)
    
    def few_shot_without_explainations(self):
        with open("../informative_samples/entity/entities-without-explaination.json","r") as f:
            few_shot_samples = json.load(f)
        few_shot_samples = few_shot_samples[:self.few_shot]
        return(few_shot_samples)

    def formatting_chatgpt_response(self, output):
        ENTITY_MAPPING = ["PERSON","LOCATION","ORGANIZATION","NORP","FACILITY","PRODUCT",
                "EVENT","WORK_OF_ART","LANGUAGE","LAW","ROLE","TITLE"]

        # Find the starting and ending indices of the JSON object
        start_index = output.find("{")
        end_index = output.rfind("}") + 1

        # Extract the JSON data
        output_refined = output[start_index:end_index+1].strip()

        if not output_refined.startswith('{'):
            output_refined="{"+output_refined
        if not output_refined.endswith('}'):
            output_refined=output_refined+"}"

        # Parse the JSON data
        output_refined = json.loads(output_refined)

        entity_dict = {key:[] for key in ENTITY_MAPPING}
        for key in ENTITY_MAPPING:
            if key in output_refined:
                for ent in output_refined[key]:
                    entity_dict[key].append(ent)
        return(entity_dict)

    def formatting_chatgpt_response_docred(self, output):
        ENTITY_MAPPING = ["PERSON","LOCATION","ORGANIZATION"]

        # Find the starting and ending indices of the JSON object
        start_index = output.find("{")
        end_index = output.rfind("}") + 1

        # Extract the JSON data
        output_refined = output[start_index:end_index+1].strip()

        if not output_refined.startswith('{'):
            output_refined="{"+output_refined
        if not output_refined.endswith('}'):
            output_refined=output_refined+"}"

        # Parse the JSON data
        output_refined = json.loads(output_refined)

        entity_dict = {key:[] for key in ENTITY_MAPPING}
        for key in ENTITY_MAPPING:
            if key in output_refined:
                for ent in output_refined[key]:
                    entity_dict[key].append(ent)
        return(entity_dict)

    def find_offset(self, text, entities):
        entity_offsets = []
        for entity_type, mentions in entities.items():
            for mention in mentions:
                pattern_exact = re.compile(re.escape(mention))
                match_exact = pattern_exact.search(text)
                if match_exact:
                    entity_offsets.append({"mention": mention, "label": entity_type, "position": {"start_offset":match_exact.start(), "end_offset":match_exact.end()}})
        return(entity_offsets)

    def consistent_checker(self, data):
        if self.consistency_count==3:
            checking = 2
        elif self.consistency_count==5:
            checking = 3

        # Initialize the new dictionary
        new_dict = {}

        # Get all keys from the dictionaries
        all_keys = set().union(*[item.keys() for item in data])

        # Iterate over each key
        for key in all_keys:
            count = sum(key in item for item in data)
            if count >= checking:
                values = set()
                for item in data:
                    values.update(item.get(key, []))
                new_dict[key] = list(values)

        return(new_dict)
