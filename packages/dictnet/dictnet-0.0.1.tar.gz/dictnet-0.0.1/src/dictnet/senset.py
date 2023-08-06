from typing import TYPE_CHECKING, Dict, List
from copy import deepcopy

if TYPE_CHECKING:
    from .dictnet import Dictnet


class Senset:
    def __init__(self, sense: Dict[str, str], dictnet: "Dictnet" = None):
        self._id = sense['id']
        self._key = sense['key']
        self._headword = sense['headword']
        self._pos = sense['pos']
        self._guideword = sense['guideword']
        self._en_def = sense['en_def']
        self._ch_def = sense['ch_def']
        self._level = sense['level']
        self._gcs = sense['gcs']
        self._examples = sense['examples']
        self._dictnet = dictnet

    @property
    def id(self) -> str:
        return self._id

    @property
    def key(self) -> str:
        return self._key

    @property
    def headword(self) -> str:
        return self._headword

    @property
    def pos(self) -> str:
        return self._pos

    @property
    def guideword(self) -> str:
        return self._guideword

    @property
    def en_def(self) -> str:
        return self._en_def

    @property
    def en_def(self) -> str:
        return self._en_def

    @property
    def ch_def(self) -> str:
        return self._ch_def

    @property
    def gcs(self) -> str:
        return self._gcs

    @property
    def examples(self) -> List[Dict[str, str]]:
        return deepcopy(self._examples)

    def __repr__(self) -> str:
        return f"Senset('{self.id}')"

    def similar_sensets(self, pos: str = None, top: int = 10) -> List["Senset"]:
        return self._dictnet.find_similar_sensets_by_id(self.id, pos, top)
