import os
import re
import json
import time
import nltk
import random
import pandas as pd
from collections import defaultdict

class REL:

    def __init__(self,few_shot=0,consistency_count=0,relation_label="None"):
        self.few_shot = few_shot
        self.consistency_count = consistency_count
        if relation_label in ["docred","ace05"]:
            self.relation_label = relation_label
        else:
            print("Either 'docred' or 'ace05'")

    def retrieve_guideline(self):
        relations_label_file = pd.read_csv(f"../guideline/{self.relation_label}.csv")
        guideline_to_prompt = ["Relation Label: {}, Label Description: {}".format(row["Relation Label"],row["Description"]) for idx, row in relations_label_file.iterrows()]
        return(guideline_to_prompt)

    def dsearch(self, lod, **kw):
        return filter(lambda i: all((i[k] == v for (k, v) in kw.items())), lod)

    def few_shot_with_explainations(self):
        with open(f"../informative_samples/relation/{self.relation_label}/relation-with-explaination.json","r") as f:
            few_shot_samples = json.load(f)
        few_shot_samples = few_shot_samples[:self.few_shot]
        return(few_shot_samples)
    
    def few_shot_without_explainations(self):
        with open(f"../informative_samples/relation/{self.relation_label}/relation-without-explaination.json","r") as f:
            few_shot_samples = json.load(f)
        few_shot_samples = few_shot_samples[:self.few_shot]
        return(few_shot_samples)

    def response_format(self, output):
        try:
            # Find the starting and ending indices of the JSON object
            start_index = output.find("{")
            end_index = output.rfind("}") + 1

            # Extract the JSON content
            json_content = output[start_index:end_index]

            # Convert the extracted JSON string to a Python dictionary
            output_dict = json.loads(json_content)
            output_refined = output_dict["annotations"]
        except:
            output_refined = "Failed to extract relation from JSON"
            print("Failed JSON Load")
        return(output_refined)

    def consistent_checker(self, response):
        if self.consistency_count == 3:
            checking = 2
        elif self.consistency_count ==5:
            checking = 3
        # Flatten the nested list
        flattened_data = [item for sublist in response for item in sublist]
        
        # Count the occurrences of each dictionary
        dictionary_counts = defaultdict(int)
        for d in flattened_data:
            dictionary_counts[str(d)] += 1
        
        # Filter out dictionaries that appear exactly 2 times
        filtered_dictionaries = [eval(key) for key, count in dictionary_counts.items() if count == checking]
        return(filtered_dictionaries)
