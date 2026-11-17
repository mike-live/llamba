from enum import Enum
from string import Template

from llamba.util.strings import en, ru

class Lang(str, Enum):
    EN = "en"
    RU = "ru"

TRANSLATIONS: dict[Lang, dict[str, str]] = {
    Lang.EN: en.TRANSLATIONS,
    Lang.RU: ru.TRANSLATIONS,
}

_current_lang: Lang = Lang.EN

def set_language(lang: Lang) -> None:
    global _current_lang
    _current_lang = lang

def get_language() -> Lang:
    return _current_lang

def get_string(key: str, **kwargs) -> str:
    template = TRANSLATIONS[_current_lang].get(key)
    if template is None:
        return f"[{key}]"
    return template.format(**kwargs) if kwargs else template