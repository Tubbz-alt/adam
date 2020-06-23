from itertools import chain

import pytest
from more_itertools import flatten

from adam.curriculum.curriculum_utils import (
    standard_object,
    phase1_instances,
    PHASE1_CHOOSER_FACTORY,
)
from adam.curriculum.phase1_curriculum import (
    _object_with_color_template,
    _x_has_y_template,
)
from adam.language_specific.english.english_language_generator import (
    GAILA_PHASE_1_LANGUAGE_GENERATOR,
)
from adam.language_specific.chinese.chinese_language_generator import (
    GAILA_PHASE_1_CHINESE_LANGUAGE_GENERATOR,
)
from adam.language_specific.english.english_language_generator import IGNORE_HAS_AS_VERB
from adam.learner import LearningExample
from adam.learner.attributes import SubsetAttributeLearner, SubsetAttributeLearnerNew
from adam.learner.integrated_learner import IntegratedTemplateLearner
from adam.learner.objects import ObjectRecognizerAsTemplateLearner
from adam.ontology import IS_SPEAKER, IS_ADDRESSEE
from adam.ontology.phase1_ontology import (
    RED,
    WHITE,
    BLACK,
    GREEN,
    BLUE,
    BALL,
    BOOK,
    GAILA_PHASE_1_ONTOLOGY,
    CAR,
    PERSON,
    INANIMATE_OBJECT,
    PERSON_CAN_HAVE,
)
from adam.situation.templates.phase1_templates import property_variable, sampled
from tests.learner import TEST_OBJECT_RECOGNIZER

OLD_SUBSET_ATTRIBUTE_LEARNER_FACTORY = lambda: SubsetAttributeLearner(
    object_recognizer=TEST_OBJECT_RECOGNIZER, ontology=GAILA_PHASE_1_ONTOLOGY
)
NEW_SUBSET_ATTRIBUTE_LEARNER_FACTORY = lambda: IntegratedTemplateLearner(
    object_learner=ObjectRecognizerAsTemplateLearner(
        object_recognizer=TEST_OBJECT_RECOGNIZER
    ),
    attribute_learner=SubsetAttributeLearnerNew(
        ontology=GAILA_PHASE_1_ONTOLOGY, beam_size=5
    ),
)

# TODO: fix integrated learner for Chinese
LEARNERS_TO_TEST = [
    OLD_SUBSET_ATTRIBUTE_LEARNER_FACTORY,
    # NEW_SUBSET_ATTRIBUTE_LEARNER_FACTORY,
]


@pytest.mark.parametrize(
    "color_node,object_0_node,object_1_node",
    [
        (RED, BALL, BOOK),
        (BLUE, BALL, BOOK),
        (GREEN, BALL, BOOK),
        (BLACK, BALL, CAR),
        (WHITE, BALL, CAR),
    ],
)
@pytest.mark.parametrize(
    "language_generator",
    [GAILA_PHASE_1_CHINESE_LANGUAGE_GENERATOR, GAILA_PHASE_1_LANGUAGE_GENERATOR],
)
def test_subset_color_attribute_learner_integrated(
    color_node, object_0_node, object_1_node, language_generator
):
    color = property_variable(f"{color_node.handle}", color_node)
    object_0 = standard_object(
        f"{object_0_node.handle}", object_0_node, added_properties=[color]
    )
    object_1 = standard_object(
        f"{object_1_node.handle}", object_1_node, added_properties=[color]
    )

    color_object_template = _object_with_color_template(object_0)

    templates = [color_object_template, _object_with_color_template(object_1)]

    color_train_curriculum = phase1_instances(
        f"{color.handle} Color Train",
        language_generator=language_generator,
        situations=chain(
            *[
                flatten(
                    [
                        sampled(
                            template,
                            chooser=PHASE1_CHOOSER_FACTORY(),
                            ontology=GAILA_PHASE_1_ONTOLOGY,
                            max_to_sample=2,
                        )
                        for template in templates
                    ]
                )
            ]
        ),
    )

    color_test_curriculum = phase1_instances(
        f"{color.handle} Color Test",
        situations=sampled(
            color_object_template,
            chooser=PHASE1_CHOOSER_FACTORY(),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
        language_generator=language_generator,
    )

    learner = IntegratedTemplateLearner(
        object_learner=ObjectRecognizerAsTemplateLearner(
            object_recognizer=TEST_OBJECT_RECOGNIZER,
            language_generator=language_generator,
        ),
        attribute_learner=SubsetAttributeLearnerNew(
            ontology=GAILA_PHASE_1_ONTOLOGY, beam_size=5
        ),
    )

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in color_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            language_generator=language_generator,
        )

    for (
        _,
        test_lingustics_description,
        test_perceptual_representation,
    ) in color_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, language_generator=language_generator
        )
        gold = test_lingustics_description.as_token_sequence()
        assert descriptions_from_learner
        assert gold in [desc.as_token_sequence() for desc in descriptions_from_learner]


@pytest.mark.parametrize(
    "color_node,object_0_node,object_1_node",
    [
        (RED, BALL, BOOK),
        (BLUE, BALL, BOOK),
        (GREEN, BALL, BOOK),
        (BLACK, BALL, CAR),
        (WHITE, BALL, CAR),
    ],
)
@pytest.mark.parametrize(
    "language_generator",
    [GAILA_PHASE_1_CHINESE_LANGUAGE_GENERATOR, GAILA_PHASE_1_LANGUAGE_GENERATOR],
)
def test_subset_color_attribute_learner_subset(
    color_node, object_0_node, object_1_node, language_generator
):
    color = property_variable(f"{color_node.handle}", color_node)
    object_0 = standard_object(
        f"{object_0_node.handle}", object_0_node, added_properties=[color]
    )
    object_1 = standard_object(
        f"{object_1_node.handle}", object_1_node, added_properties=[color]
    )

    color_object_template = _object_with_color_template(object_0)

    templates = [color_object_template, _object_with_color_template(object_1)]

    color_train_curriculum = phase1_instances(
        f"{color.handle} Color Train",
        language_generator=language_generator,
        situations=chain(
            *[
                flatten(
                    [
                        sampled(
                            template,
                            chooser=PHASE1_CHOOSER_FACTORY(),
                            ontology=GAILA_PHASE_1_ONTOLOGY,
                            max_to_sample=2,
                        )
                        for template in templates
                    ]
                )
            ]
        ),
    )

    color_test_curriculum = phase1_instances(
        f"{color.handle} Color Test",
        situations=sampled(
            color_object_template,
            chooser=PHASE1_CHOOSER_FACTORY(),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
        language_generator=language_generator,
    )

    learner = OLD_SUBSET_ATTRIBUTE_LEARNER_FACTORY()

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in color_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            language_generator=language_generator,
        )

    for (
        _,
        test_lingustics_description,
        test_perceptual_representation,
    ) in color_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, language_generator=language_generator
        )
        gold = test_lingustics_description.as_token_sequence()
        assert descriptions_from_learner
        assert gold in [desc.as_token_sequence() for desc in descriptions_from_learner]


# hack: wo de and ni de are currently considered to be one word. This won't work for third person possession
@pytest.mark.parametrize(
    "language_generator",
    [GAILA_PHASE_1_LANGUAGE_GENERATOR, GAILA_PHASE_1_CHINESE_LANGUAGE_GENERATOR],
)
def test_subset_my_attribute_learner_integrated(language_generator):
    person = standard_object("speaker", PERSON, added_properties=[IS_SPEAKER])
    inanimate_object = standard_object(
        "object", INANIMATE_OBJECT, required_properties=[PERSON_CAN_HAVE]
    )

    my_train_curriculum = phase1_instances(
        "my-train",
        situations=sampled(
            _x_has_y_template(
                person, inanimate_object, syntax_hints=[IGNORE_HAS_AS_VERB]
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=2,
        ),
        language_generator=language_generator,
    )

    my_test_curriculum = phase1_instances(
        "my-test",
        situations=sampled(
            _x_has_y_template(
                person, inanimate_object, syntax_hints=[IGNORE_HAS_AS_VERB]
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=1,
        ),
        language_generator=language_generator,
    )

    learner = IntegratedTemplateLearner(
        object_learner=ObjectRecognizerAsTemplateLearner(
            object_recognizer=TEST_OBJECT_RECOGNIZER,
            language_generator=language_generator,
        ),
        attribute_learner=SubsetAttributeLearnerNew(
            ontology=GAILA_PHASE_1_ONTOLOGY, beam_size=5
        ),
    )

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in my_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            language_generator=language_generator,
        )

    for (
        _,
        test_lingustics_description,
        test_perceptual_representation,
    ) in my_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, language_generator=language_generator
        )
        gold = test_lingustics_description.as_token_sequence()
        assert descriptions_from_learner
        assert gold in [desc.as_token_sequence() for desc in descriptions_from_learner]


@pytest.mark.parametrize(
    "language_generator",
    [GAILA_PHASE_1_LANGUAGE_GENERATOR, GAILA_PHASE_1_CHINESE_LANGUAGE_GENERATOR],
)
def test_subset_my_attribute_learner_subset(language_generator):
    person = standard_object("speaker", PERSON, added_properties=[IS_SPEAKER])
    inanimate_object = standard_object(
        "object", INANIMATE_OBJECT, required_properties=[PERSON_CAN_HAVE]
    )

    my_train_curriculum = phase1_instances(
        "my-train",
        situations=sampled(
            _x_has_y_template(
                person, inanimate_object, syntax_hints=[IGNORE_HAS_AS_VERB]
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=2,
        ),
        language_generator=language_generator,
    )

    my_test_curriculum = phase1_instances(
        "my-test",
        situations=sampled(
            _x_has_y_template(
                person, inanimate_object, syntax_hints=[IGNORE_HAS_AS_VERB]
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=1,
        ),
        language_generator=language_generator,
    )

    learner = OLD_SUBSET_ATTRIBUTE_LEARNER_FACTORY()

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in my_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            language_generator=language_generator,
        )

    for (
        _,
        test_lingustics_description,
        test_perceptual_representation,
    ) in my_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, language_generator=language_generator
        )
        gold = test_lingustics_description.as_token_sequence()
        assert descriptions_from_learner
        assert gold in [desc.as_token_sequence() for desc in descriptions_from_learner]


@pytest.mark.parametrize(
    "language_generator",
    [GAILA_PHASE_1_CHINESE_LANGUAGE_GENERATOR, GAILA_PHASE_1_LANGUAGE_GENERATOR],
)
def test_your_attribute_learner_subset(language_generator):
    person_0 = standard_object("speaker", PERSON, added_properties=[IS_SPEAKER])
    person_1 = standard_object("addressee", PERSON, added_properties=[IS_ADDRESSEE])
    inanimate_object = standard_object(
        "object", INANIMATE_OBJECT, required_properties=[PERSON_CAN_HAVE]
    )

    your_train_curriculum = phase1_instances(
        "your-train",
        situations=sampled(
            _x_has_y_template(
                person_1,
                inanimate_object,
                background=[person_0],
                syntax_hints=[IGNORE_HAS_AS_VERB],
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=2,
        ),
        language_generator=language_generator,
    )

    your_test_curriculum = phase1_instances(
        "your-test",
        situations=sampled(
            _x_has_y_template(
                person_1,
                inanimate_object,
                background=[person_0],
                syntax_hints=[IGNORE_HAS_AS_VERB],
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=1,
        ),
        language_generator=language_generator,
    )

    learner = OLD_SUBSET_ATTRIBUTE_LEARNER_FACTORY()

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in your_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            language_generator=language_generator,
        )

    for (
        _,
        test_lingustics_description,
        test_perceptual_representation,
    ) in your_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, language_generator=language_generator
        )
        gold = test_lingustics_description.as_token_sequence()
        assert descriptions_from_learner
        assert gold in [desc.as_token_sequence() for desc in descriptions_from_learner]


@pytest.mark.parametrize(
    "language_generator",
    [GAILA_PHASE_1_CHINESE_LANGUAGE_GENERATOR, GAILA_PHASE_1_LANGUAGE_GENERATOR],
)
def test_your_attribute_learner_integrated(language_generator):
    person_0 = standard_object("speaker", PERSON, added_properties=[IS_SPEAKER])
    person_1 = standard_object("addressee", PERSON, added_properties=[IS_ADDRESSEE])
    inanimate_object = standard_object(
        "object", INANIMATE_OBJECT, required_properties=[PERSON_CAN_HAVE]
    )

    your_train_curriculum = phase1_instances(
        "your-train",
        situations=sampled(
            _x_has_y_template(
                person_1,
                inanimate_object,
                background=[person_0],
                syntax_hints=[IGNORE_HAS_AS_VERB],
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=2,
        ),
        language_generator=language_generator,
    )

    your_test_curriculum = phase1_instances(
        "your-test",
        situations=sampled(
            _x_has_y_template(
                person_1,
                inanimate_object,
                background=[person_0],
                syntax_hints=[IGNORE_HAS_AS_VERB],
            ),
            ontology=GAILA_PHASE_1_ONTOLOGY,
            chooser=PHASE1_CHOOSER_FACTORY(),
            max_to_sample=1,
        ),
        language_generator=language_generator,
    )

    learner = IntegratedTemplateLearner(
        object_learner=ObjectRecognizerAsTemplateLearner(
            object_recognizer=TEST_OBJECT_RECOGNIZER,
            language_generator=language_generator,
        ),
        attribute_learner=SubsetAttributeLearnerNew(
            ontology=GAILA_PHASE_1_ONTOLOGY, beam_size=5
        ),
    )

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in your_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            language_generator=language_generator,
        )

    for (
        _,
        test_lingustics_description,
        test_perceptual_representation,
    ) in your_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, language_generator=language_generator
        )
        gold = test_lingustics_description.as_token_sequence()
        assert descriptions_from_learner
        assert gold in [desc.as_token_sequence() for desc in descriptions_from_learner]
