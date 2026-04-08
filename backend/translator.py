import json

LANG = json.load(open("config/languages.json", "r", encoding="utf-8"))

def t(key, lang):
    return LANG.get(lang, LANG["en"]).get(key, key)
