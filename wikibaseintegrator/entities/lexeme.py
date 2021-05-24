from __future__ import annotations

from wikibaseintegrator.entities.baseentity import BaseEntity
from wikibaseintegrator.models.forms import Forms
from wikibaseintegrator.models.lemmas import Lemmas
from wikibaseintegrator.models.senses import Senses


class Lexeme(BaseEntity):
    def __init__(self, api, lemmas=None, lexical_category=None, language=None, forms=None, senses=None, **kwargs):
        self.api = api

        super().__init__(api=self.api, entity_type='lexeme', **kwargs)

        self.lemmas = lemmas or Lemmas()
        self.lexicalCategory = lexical_category
        self.language = language or self.api.language
        self.forms = forms or Forms()
        self.senses = senses or Senses()

    def get(self, entity_id) -> Lexeme:
        json_data = super(Lexeme, self).get(entity_id=entity_id)
        return Lexeme(self.api).from_json(json_data=json_data['entities'][entity_id])

    def set(self, **kwargs) -> Lexeme:
        self.__init__(self.api, **kwargs)
        return self

    def get_json(self) -> {}:
        return {
            'lemmas': self.lemmas.get_json(),
            'lexicalCategory': self.lexicalCategory,
            'language': self.language,
            'forms': self.forms.get_json(),
            'senses': self.senses.get_json(),
            **super(Lexeme, self).get_json()
        }

    def from_json(self, json_data) -> Lexeme:
        super(Lexeme, self).from_json(json_data=json_data)

        self.lemmas = Lemmas().from_json(json_data['lemmas'])
        self.lexicalCategory = json_data['lexicalCategory']
        self.language = json_data['language']
        self.forms = Forms().from_json(json_data['forms'])
        self.senses = Senses().from_json(json_data['senses'])

        return self

    def write(self):
        json_data = super(Lexeme, self)._write(data=self.get_json())
        return self.from_json(json_data=json_data)
