from . import exceptions

# define token extractor names & defaults
EXTRACTOR_ISUPPER = "isupper"
EXTRACTOR_ISTITLE = "istitle"
EXTRACTOR_ISDIGIT = "isdigit"
DEFAULT_EXTRACTORS = [EXTRACTOR_ISUPPER, EXTRACTOR_ISTITLE, EXTRACTOR_ISDIGIT]

# define feature layers & defaults
FEATURE_LAYER_WORD = "word"
FEATURE_LAYER_LEMMA = "lemma"
FEATURE_LAYER_POS = "pos_tag"
DEFAULT_LAYERS = [FEATURE_LAYER_WORD, FEATURE_LAYER_LEMMA, FEATURE_LAYER_POS]


def extract_features(item, layers_to_use, extractors_to_use, word_index):
    """
    Extract features from token and surrounding tokens based on window size.
    """
    features = []
    # select features from selected layers
    for layer in layers_to_use:
        if layer not in item:
            raise exceptions.InvalidInputError(f"Layer {layer} not present in document!")
        value = item[layer].lower()
        features.append(f"{word_index}:{layer}={value}")
    # extract more features from token
    token = item["word"]
    for extractor in extractors_to_use:
        if extractor == EXTRACTOR_ISUPPER:
            feature_value = token.isupper()
            features.append(f"{word_index}:word.{extractor}={feature_value}")
        elif extractor == EXTRACTOR_ISTITLE:
            feature_value = token.istitle()
            features.append(f"{word_index}:word.{extractor}={feature_value}")
        elif extractor == EXTRACTOR_ISDIGIT:
            feature_value = token.isdigit()
            features.append(f"{word_index}:word.{extractor}={feature_value}")
        # add more extractors here!
    return features



def word2features(sent, i, config):
    # empty list for all features
    features = []
    # add bias
    if config.bias:
        features.append("bias")
    # this is the current token
    item = {
        "word": sent[i][0],
        "lemma": sent[i][1],
        "pos_tag": sent[i][2]
    }    
    features.extend(extract_features(item, config.feature_layers, config.feature_extractors, "0"))
    # check if not the first token in sentence
    if i > 0:
        for window in range(1, config.window_size+1):
            try:
                item1 = {
                    "word": sent[i-window][0],
                    "lemma": sent[i-window][1],
                    "pos_tag": sent[i-window][2]
                }
                features.extend(extract_features(item1, config.context_feature_layers, config.context_feature_extractors, f"-{window}"))
            except:
                IndexError
    else:
        # beginning of sentence
        features.append("BOS")
    # check if not the last token in sentence
    if i < len(sent)-1:
        for window in range(1, config.window_size+1):
            try:
                item1 = {
                    "word": sent[i+window][0],
                    "lemma": sent[i+window][1],
                    "pos_tag": sent[i+window][2]
                }
                features.extend(extract_features(item1, config.context_feature_layers, config.context_feature_extractors, f"+{window}"))
            except:
                IndexError
    else:
        # end of sentence
        features.append("EOS")
    return features


def sent2features(sent, config):
    return [word2features(sent, i, config) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, lemma, postag, label in sent]
