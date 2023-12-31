import json
from nltk import agreement
from urllib import request, parse
import json,urllib.request
import requests
import re
import os
import tempfile
from bratiaa.agree import F1Agreement, partial, input_generator
from bratiaa.evaluation import exact_match_token_evaluation,exact_match_instance_evaluation

def get_docs_from_json(folder_path=None):
    lines=[]
    fh = open(folder_path)
    for line in fh:
        lines.append(json.loads(line))
    fh.close()
    return lines


def get_docs_from_doccano(url_):
    host=url_[0]
    user_=url_[1]
    pass_=url_[2]
    project_=url_[3]
    ##getting token

    auth_url=host+"v1/auth/login/"
    data = {'username': user_, 'password': pass_}
    req = request.Request(auth_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    result = request.urlopen(req, jsondataasbytes).read()
    token=json.loads(result)["key"]
    header = {'Content-Type': 'application/json; charset=utf-8','Authorization': 'Token '+str(token)}

    data_url=host+"v1/projects/"+str(project_)+"/docs/download"
    # req =  request.Request(data_url, headers=header)
    # webURL = request.urlopen(req)
    req_payload = {"format":"JSONL(relation)","exportApproved":"false"}
    req = requests.post(data_url,params=req_payload)

    data=[]
    for line in webURL:
        data.append(json.loads(line.decode("utf-8")))
    return data


def get_labels(docs):
    labels_=[]
    spans_={}
    users_=[]
    docs = docs[0]
    for i in range(len(docs)):
        doc=docs[i]
        if ("annotations" in list(doc.keys())):
            text=doc["text"]
            labels=doc["annotations"]
            for label in labels:
                user_=label["user"]
                type_=str(label["label"])
                token_=str(i)+"_"+str(label["start_offset"])+"_"+str(label["end_offset"])
                if user_ not in users_:
                    users_.append(user_)
                if token_ not in spans_.keys():
                    spans_[token_]={}
                spans_[token_][user_]=type_
        else:
            calc("did not find annotations in record "+str(i))
    for key, value in spans_.items():
        for u in users_:
            if (u in spans_[key].keys() ):
                labels_.append((str(u),key, int(spans_[key][u]) ))
            else:
                labels_.append((str(u),key, 0))
    if len(labels_)==0:
        print ("no labels found")
    return labels_


def docs_to_ann(docs):
    import tempfile
    import shutil
    temp_dir = tempfile.mkdtemp()
    #print(temp_dir)
    labels_=[]
    annotators_=[]
    files_=[]
    texts_=[]
    docs = docs[0]
    for i in range(len(docs)):
        doc=docs[i]
        #replacing "\n\t" with " " to avoid error "bratsubset.annotation.InvalidIdError: Invalid id:"
        #text=doc["text"]
        text=re.sub(r"[\t]+", " ", doc["text"])
        texts_.append(text)
        if ("annotations" in list(doc.keys())):
            labels=doc["annotations"]
            users_={}
            for label in labels:
                user_=label["user"]
                type_=str(label["label"])
                labels_.append(type_)
                annotators_.append(str(user_))
                start_=label["start_offset"]
                end_=label["end_offset"]
                sub_text=text[int(start_):][:int(end_-start_)]
                if user_ not in users_.keys():
                    users_[user_]=[]
                nonono = "x" * int(int(end_)-int(start_))
                users_[user_].append(["T"+str(len(users_[user_])+1),type_,start_,end_,sub_text])

        for u,values in users_.items():
            dir_user=str(temp_dir)+"/"+str(u)
            file_dir_user=dir_user+"/"+str(i+1)+".ann"
            os.makedirs(dir_user, exist_ok=True)
            files_.append(str(i+1)+".ann")
            with open(file_dir_user, 'w', encoding="utf-8") as f:
                for v in values:
                    line=str(v[0])+"\t"+str(v[1])+" "+str(v[2])+" "+str(v[3])+"\t"+str(v[4])
                    f.write(line+"\n")
            ##add txt files
            with open(dir_user+"/"+str(i+1)+".txt", 'w', encoding="utf-8") as f:
                f.write(text+"\n")

    #making sure that we have same TXT files in each dir
    for i in range(len(texts_)):
        for u in list(set(annotators_)):
            file_=temp_dir+"/"+str(u)+"/"+str(i+1)+".txt"
            #annotation
            with open(file_, 'w', encoding="utf-8") as f:
                f.write(texts_[i]+"\n")


    #making sure that we have same ANN files in each dir
    for f in list(set(files_)):
        for a in list(set(annotators_)):
            file_dir=temp_dir+"/"+str(a)+"/"+str(f)
            #annotation
            open(file_dir, 'a+')
    #print (temp_dir)
    return temp_dir,list(set(labels_)),list(set(annotators_)),list(set(files_))


def compute_f1_scores(docs):
    project,labels,annotators,docs = docs_to_ann(docs)
    

    def token_func(text):
        token = re.compile('\w+|[^\w\s]+')
        for match in re.finditer(token, text):
            yield match.start(), match.end()


    agg=F1Agreement(partial(input_generator, project), labels,annotators=annotators, documents=docs, token_func=token_func,
                    eval_func=exact_match_token_evaluation)
    return agg


def calc(labels):
    metrics={}
    ratingtask = agreement.AnnotationTask(data=labels)
    metrics["kappa"]=ratingtask.kappa()
    metrics["fleiss"]=ratingtask.multi_kappa()
    metrics["alpha"]=ratingtask.alpha()
    metrics["scotts"]=ratingtask.pi()
    return metrics