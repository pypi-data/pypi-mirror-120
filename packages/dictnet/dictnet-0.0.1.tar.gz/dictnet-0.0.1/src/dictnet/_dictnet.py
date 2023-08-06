from typing import Dict, List
from gensim.models import KeyedVectors
from .senset import Senset


class Dictnet:
    def __init__(self, senses: List[Dict[str, str]], def_embeds: KeyedVectors):
        self._def_embeds = def_embeds
        self._pos_to_sensets, self._headword_to_sensets, self._id_to_sensets = self._load_sensets(
            senses)

    def _load_sensets(self, senses: List[Dict[str, str]]):
        pos_to_sensets = {}
        headword_to_sensets = {}
        id_to_sensets = {}
        for sense in senses:
            if sense['id'] not in self._def_embeds:
                continue
            headword = sense['headword']
            pos = sense['pos']
            if pos not in pos_to_sensets:
                pos_to_sensets[pos] = []
            if headword not in headword_to_sensets:
                headword_to_sensets[headword] = []
            senset = Senset(sense, self)
            pos_to_sensets[pos].append(senset)
            headword_to_sensets[headword].append(senset)
            id_to_sensets[senset.id] = senset
        return (pos_to_sensets, headword_to_sensets, id_to_sensets)

    def keys(self, pos: str = None) -> List[str]:
        self._validate_pos(pos)
        if pos is None:
            return list(set(senset.key for sensets in self._pos_to_sensets.values()
                            for senset in sensets))
        else:
            return list(set(senset.key for senset in self._pos_to_sensets[pos]))

    def headwords(self, pos: str = None) -> List[str]:
        self._validate_pos(pos)
        if pos is None:
            return list(set(senset.headword for sensets in self._pos_to_sensets.values()
                            for senset in sensets))
        else:
            return list(set(senset.headword for senset in self._pos_to_sensets[pos]))

    def all_sensets(self, pos: str = None) -> List[Senset]:
        self._validate_pos(pos)
        if pos is None:
            return [senset for sensets in self._pos_to_sensets.values()
                    for senset in sensets]
        else:
            return [senset for senset in self._pos_to_sensets[pos]]

    def sensets(self, headword: str, pos: str = None) -> List[Senset]:
        self._validate_headword(headword)
        self._validate_pos(pos)
        sensets = self._headword_to_sensets[headword]
        if pos is None:
            return sensets
        else:
            return [senset for senset in sensets
                    if senset.pos == pos]

    def senset(self, senset_id: str) -> Senset:
        self._validate_senset_id(senset_id)
        return self._id_to_sensets[senset_id]

    def find_similar_sensets_by_id(self, senset_id: str,
                                   pos: str = None, top: int = 10) -> List[Senset]:
        self._validate_senset_id(senset_id)
        self._validate_pos(pos)
        if pos is None:
            return [self.senset(_id) for _id, _ in self._def_embeds.most_similar(senset_id, topn=top)]
        else:
            sensets = []
            candidates = self._def_embeds.most_similar(
                senset_id, topn=len(self._def_embeds.vocab))
            for _id, _ in candidates:
                if len(sensets) >= top:
                    break
                senset = self.senset(_id)
                if senset.pos == pos:
                    sensets.append(senset)
            return sensets

    def _validate_pos(self, pos):
        if pos is not None and pos not in self._pos_to_sensets:
            raise KeyError(
                f'{pos} is not in the pos tags: {list(self._pos_to_sensets.keys())}')
        return

    def _validate_headword(self, headword: bool):
        if headword not in self._headword_to_sensets:
            raise KeyError(f'{headword} is not in the sensets')
        return

    def _validate_senset_id(self, senset_id: str):
        if senset_id not in self._def_embeds:
            raise KeyError(f'{senset_id} is not in the sensets')
        return
