####for running the file you have to specify python custom_ner_build_model.py en <model_name> <drop-ratio> &
### set the drop ratio from 0.5 to 0.8 for better results and less noise value

from __future__ import unicode_literals, print_function
from db import *
import random
from pathlib import Path
import random
import json
import spacy
from spacy.gold import GoldParse
from spacy.tagger import Tagger
from datetime import datetime

def train_ner(nlp, train_data, output_dir,drop_ratio):

    for raw_text, _ in train_data:
        doc = nlp.make_doc(raw_text)
        for word in doc:
            _ = nlp.vocab[word.orth]
    random.seed(0)

    nlp.entity.model.learn_rate = 0.001

    #define the no of backward loops
    for itn in range(10):
        start=datetime.now()
        print(start)
        random.shuffle(train_data)
        loss = 0.
        for raw_text, entity_offsets in train_data:
            doc = nlp.make_doc(raw_text)
            gold = GoldParse(doc, entities=entity_offsets)
            nlp.tagger(doc)

            loss += nlp.entity.update(doc, gold, drop=float(drop_ratio))
        print(datetime.now()-start)
        if loss == 0:
            break

    nlp.end_training()
    if output_dir:
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.save_to_directory(output_dir)


def main(model_name, output_directory=None,drop_ratio=None):
    print("Loading initial model", model_name)
    nlp = spacy.load(model_name)
    if output_directory is not None:
        output_directory = Path(output_directory)
    l = test_data_job_information.find({})
    train_data1=[]
    train_data2=[]
    for i in l:
        train_data1.append(i["soup_processed_data"])
        train_data2.append(i["train_data"][1]["entities"])
    train_data=zip(train_data1,train_data2)

    nlp.entity.add_label('TECHNICAL_SKILL')
    train_ner(nlp, train_data, output_directory,drop_ratio)

    test_data_obj=test_data_job_information.find({})
    if output_directory:
        print("Loading from", output_directory)
        nlp2 = spacy.load('en', path=output_directory)
        nlp2.entity.add_label('TECHNICAL_SKILL')

        for data in test_data_obj:
            output_test_data=[]
            doc2 = nlp2(data["train_data"][0])
            for ent in doc2.ents:
                if ent.text not in output_test_data:
                    output_test_data.append(ent.text)



if __name__ == '__main__':
    import plac
    plac.call(main)