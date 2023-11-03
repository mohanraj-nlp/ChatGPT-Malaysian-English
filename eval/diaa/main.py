#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
from diaa.maker import *
import operator
import bratiaa as biaa

def main(path):
    docs = get_docs_from_json(path)
    labels=get_labels(docs)
    agg=compute_f1_scores(docs)
    biaa.iaa_report(agg)
    agreement=calc(labels)
    return(agreement)