#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

try:
    import fasttext
except:
    pass

FT_MODEL = None
PROJ_DIR = Path(__file__).parent.parent
MODEL_PATH = PROJ_DIR / 'lang_detector' / 'lid.176.ftz'

def text_preprocess(text):
    return text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()

def get_language(text, top_k=1):
    global FT_MODEL
    if top_k < 1 or top_k > 176:
        raise ValueError("top_k must be between 1 and 176, "
                         "it's the number of languages supported by fasttext")
    if FT_MODEL is None:
        FT_MODEL = fasttext.load_model(str(MODEL_PATH))
    langs, probs = FT_MODEL.predict(text_preprocess(text), top_k)
    if top_k > 1:
        return [{
            'lang': lang.replace('__label__', ''),
            'prob': prob
        } for lang, prob in zip(langs, probs)]
    else:
        return {
            'lang': langs[0].replace('__label__', ''),
            'prob': probs[0]
        }
