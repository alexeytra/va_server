from yargy import (
    Parser,
    rule, or_
)
from yargy.pipelines import morph_pipeline
from yargy.interpretation import (
    fact,
    attribute
)
from yargy.tokenizer import MorphTokenizer, EOL
from constants.constants import DEPARTMENTS, CLASSROOMS, BUILDINGS

class EntityExtractor:
    def __init__(self) -> None:
        self.__Intro = fact(
            'Intro',
            [
                attribute('kaf'),
                attribute('auditorium'),
                attribute('building'),
            ]
        )
        self.__rule_build()

    def __rule_build(self):
        DEPARTMENT = morph_pipeline(DEPARTMENTS).interpretation(
            self.__Intro.kaf.normalized().custom(DEPARTMENTS.get)
        )
        CLASSROOM = morph_pipeline(CLASSROOMS).interpretation(
            self.__Intro.auditorium.custom(CLASSROOMS.get)
        )
        BUILD = morph_pipeline(BUILDINGS).interpretation(
            self.__Intro.building.normalized().custom(BUILDINGS.get)
        )

        self.__INTRO = rule(
            or_(
                DEPARTMENT,
                CLASSROOM,
                BUILD
                )
        ).interpretation(self.__Intro)

    def extract_entity(self, text):
        TOKENIZER = MorphTokenizer().remove_types(EOL)
        parser = Parser(self.__INTRO, tokenizer=TOKENIZER)
        matches = list(parser.findall(text))
        if matches:
            match = matches[0]
            result = [_.value for _ in match.tokens]
            entity = ' '.join(map(str, result))
            facts = match.fact
            fact = list(filter(lambda f: (f != None), facts ))
            _type, key = fact[0].split('_')
            return {
                'entity': entity,
                'key': key,
                'type': _type
            }
        return {}