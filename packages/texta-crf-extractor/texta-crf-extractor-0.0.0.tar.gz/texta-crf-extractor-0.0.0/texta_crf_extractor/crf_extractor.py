import joblib
import json
import pycrfsuite
import uuid
import os
from sklearn.model_selection import train_test_split
from typing import List, Union, Dict, Tuple

from .config import CRFConfig
from .feature_extraction import sent2features, sent2labels
from .tagging_report import TaggingReport
from . import exceptions


def check_model_loaded(func):
    """
    Wrapper function for checking if Tagger model is loaded.
    """
    def func_wrapper(*args, **kwargs):
        if not args[0].model:
            raise exceptions.ModelNotLoadedError()
        return func(*args, **kwargs)
    return func_wrapper


class CRFExtractor:

    def __init__(self, description="My CRF Extractor", labels=["GPE", "ORG", "PER", "LOC"], mlp=None, config=CRFConfig()):
        self.description = description
        self.labels = labels
        self.mlp = mlp
        self.model = None
        self.config = config


    def __str__(self):
        return self.description


    @staticmethod
    def _validate_mlp_structure(mlp_document, field_name):
        """
        Validates the MLP document structure to have proper fields.
        """

        # TODO: add content check as well. + nested docs, ugh!

        if not isinstance(mlp_document, dict):
            raise exceptions.InvalidInputError("Input not dict!")
        if field_name not in mlp_document:
            raise exceptions.InvalidInputError(f"Field '{field_name}' not present in the document!")
    
        # check if mlp fields are present
        fields_to_check = ["text", "lemmas", "pos_tags"]
        for field in fields_to_check:
            if field not in mlp_document[field_name]:
                raise exceptions.InvalidInputError(f"Field '{field}' not present in the document!")


    def _parse_mlp_document(self, mlp_document, add_labels=True, text_field="text"):
        """
        Parses MLP output document. Extracts tokens, lemmas, and POS tags.
        Adds labels from texta_facts.
        """
        self._validate_mlp_structure(mlp_document, text_field)
        
        # TODO: Handling of nested documents

        text = mlp_document[text_field]["text"]
        tokens = text.split(" ")
        lemmas = mlp_document[text_field]["lemmas"].split(" ")
        pos_tags = mlp_document[text_field]["pos_tags"].split(" ")

        # add labels from texta_facts
        if add_labels:
            texta_facts = mlp_document.get("texta_facts", [])
            # create initial label list
            labels = ["0" for x in range(len(tokens))]
            # ectract labels from facts
            for fact in mlp_document["texta_facts"]:
                if fact["fact"] in self.labels:
                    label = fact["fact"]
                    # retrieve original spans for the entities
                    spans = json.loads(fact["spans"])
                    for span in spans:
                        num_tokens_before_match = len([token for token in text[:span[0]].split(" ") if token])
                        num_tokens_match = len(fact["str_val"].split(" "))
                        # replace initial labels with correct ones
                        for i in range(num_tokens_before_match, num_tokens_before_match+num_tokens_match):
                            labels[i] = label
            # convert document format
            return [(token, lemmas[i], pos_tags[i], labels[i]) for i, token in enumerate(tokens)]

        # convert document format
        return [(token, lemmas[i], pos_tags[i]) for i, token in enumerate(tokens)]


    def train(self, mlp_documents, text_field="text", save_path="my_crf_model"):
        """
        Trains & saves the model.
        Model has to be saved by the crfsuite package because it contains C++ bindings.
        """
        # prepare data
        # a list containing tokenized documents for CRF
        token_documents = [self._parse_mlp_document(mlp_document, text_field=text_field) for mlp_document in mlp_documents]
        # split dataset
        train_documents, test_documents = train_test_split(token_documents, test_size=self.config.test_size)
        # featurize sequences
        X_train = [sent2features(s, self.config) for s in train_documents]
        y_train = [sent2labels(s) for s in train_documents]
        X_test = [sent2features(s, self.config) for s in test_documents]
        y_test = [sent2labels(s) for s in test_documents]
        # create trainer
        trainer = pycrfsuite.Trainer(verbose=self.config.verbose)
        # feed data to trainer
        for xseq, yseq in zip(X_train, y_train):
            trainer.append(xseq, yseq)
        # set trainer params
        trainer.set_params({
            'c1': self.config.c1, # coefficient for L1 penalty
            'c2': self.config.c2, # coefficient for L2 penalty
            'max_iterations': self.config.num_iter, # stop earlier
            'feature.possible_transitions': True # include transitions that are possible, but not observed
        })
        # train & save the model
        trainer.train(save_path)
        # load tagger model for validation
        tagger = pycrfsuite.Tagger()
        tagger.open(save_path)
        # evaluate model
        y_pred = [tagger.tag(xseq) for xseq in X_test]
        report = TaggingReport(y_test, y_pred)
        # model & report to class variables
        self.model = tagger
        self.report = report
        return report, save_path


    @check_model_loaded
    def tag(self, text):
        """
        Tags input text.
        """
        # apply mlp
        mlp_output = self.mlp.process(text)
        # mlp ooutput to sequence
        seq_to_predict = self._parse_mlp_document(mlp_output, add_labels=False)
        # sequence to features
        features_to_predict = sent2features(seq_to_predict, self.config)
        # predict
        result = self.model.tag(features_to_predict)
        # generate text tokens for final output
        text_tokens = mlp_output["text"]["text"].split(" ")
        return self._process_tag_output(result, text_tokens)


    def _process_tag_output(self, tokens, text_tokens):
        """
        Translates result tokens into entities.
        """
        entities = []
        entity_types = []
        current_entity = []
        current_entity_type = None
        # iterate over tokens and pick matches
        for i, token in enumerate(tokens):
            if token in self.labels:
                entity = text_tokens[i]
                current_entity_type = token
                current_entity.append(entity)
            else:
                if current_entity:
                    entities.append({current_entity_type: " ".join(current_entity)})
                    current_entity = []
        if current_entity:
            entities.append({current_entity_type: " ".join(current_entity)})
        return entities


    def load(self, file_path):
        """
        Loads CRF model from disk.
        :param str file_path: Path to the model file.
        """
        tagger = pycrfsuite.Tagger()
        tagger.open(file_path)
        self.model = tagger
        return True
