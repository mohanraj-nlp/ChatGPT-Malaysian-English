# ChatGPT-Malaysian-English

#### Research Paper: How well ChatGPT understand Malaysian English? An Evaluation on Named Entity Recognition and Relation Extraction [[Paper Link]](https://arxiv.org/abs/2311.11583), [[Poster]](https://github.com/mohanraj-nlp/ChatGPT-Malaysian-English/blob/main/GEM-Poster-EMNLP-v2.pdf)
## Repository Structure

There are total of 90 Experiments has been conducted. This 90 Experiments are based on different NLP Task (NER or Relation Extraction), different Dataset (MEN-Dataset, DocRED), and different prompt settings (experimented with 18 different prompt settings.). The 90 experiments is conducted in seperate Jupyter Notebook.

- ner.py: Includes the function to read guideline, few shot samples and ChatGPT output formatting for **Evaluation with NER Task**.
- rel.py: Includes the function to read guideline, few shot samples and ChatGPT output formatting for **Evaluation with Relation Extraction Task**.
- notebook-men-ner, notebook-men-rel-docred, notebook-men-rel-ace05: Has all the notebooks that run for MEN-Dataset. 
- notebook-docred-ner, notebook-docred-rel-docred: Has all the notebooks that run for DocRED-Dataset.
- informative_samples: Includes FewShot samples. 
- guideline: Includes the Annotation Guideline. 
- dataset: Includes the Annotated Dataset. For this experiment we only use MEN-Dataset and DocRED.
- eval: This folder have the Jupyter Notebook to evaluate the ChatGPT outcome. We have evaluated (made some changes) using source code from [diaa](https://github.com/vwoloszyn/diaa)
- auto-chatgpt: This module used run and interact with ChatGPT web version. The source code is updated and changed, so it will suit for this experiment. Github Link for [auto-chatgpt](https://github.com/ryuseisan/auto-chatgpt)
## Run Locally
#### Kindly follow below steps in given order.
Clone the project

```bash
  git clone <annoymized_github>
```

Go to the project directory

```bash
  cd ChatGPT-Malaysian-English
```

Go to auto-chatgpt directory and install this particular module dependecies

```bash
  pip install .
```

Go back to home directory

```bash
  cd..
```

Install other library

```bash
  pip install -r requirements.txt
```

**Kindly follow the above steps, in the suggested order.** You can ignore any dependency errors.

Now Open any Jupyter Notebook File and get the output from ChatGPT. 

## ChatGPT

The input and output for ChatGPT is communicated via Selenium Bot. It is advisable to run browser with interface, as this will avoid any errors caused. In every Jupyter Notebook we have given guide on how to handle auto-chagpt (Selenium Bot).


## Evaluation

For both NER and RE, we have used F1-Score as evaluation metrics. Here is how you can run the evaluation:
- Locate the ChatGPT outcome that are saved as JSON file. 
- Copy the link and paste in the eval/Evaluating ChatGPT NER Task - MEN-Dataset.ipynb (When evaluating on MEN Dataset), eval/Evaluating ChatGPT NER Task - DocRED-Dataset.ipynb (When evaluating on DocRED Dataset) or eval/Evaluating ChatGPT Relation Extraction Task.ipynb (When evaluating on any Relation Extraction Task)

### Note: MEN-Dataset comprises Malaysian English news articles meticulously annotated with entities and relations. Presently, the dataset has been submitted for review at various conference venues. To avoid potential conflicts, we have opted not to include the dataset in this repository at this time. Upon receiving feedback regarding the dataset, we will promptly provide the link for access.
