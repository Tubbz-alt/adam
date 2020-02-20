import random

import pytest
from immutablecollections import immutableset
from more_itertools import first

from adam.curriculum.curriculum_utils import (
    standard_object,
    phase1_instances,
    PHASE1_CHOOSER,
)
from adam.curriculum.preposition_curriculum import (
    _on_template,
    _beside_template,
    _under_template,
    _over_template,
    _in_template,
    _behind_template,
    _in_front_template,
)
from adam.learner import LearningExample
from adam.learner.object_recognizer import ObjectRecognizer
from adam.learner.pursuit import PrepositionPursuitLearner
from adam.ontology import IS_ADDRESSEE, IS_SPEAKER
from adam.ontology.phase1_ontology import (
    BALL,
    TABLE,
    GAILA_PHASE_1_ONTOLOGY,
    WATER,
    CUP,
    LEARNER,
    MOM,
)
from adam.perception.perception_graph import PerceptionGraphPattern
from adam.situation.templates.phase1_templates import sampled, object_variable


def test_pursuit_preposition_on_learner():
    rng = random.Random()
    rng.seed(0)
    learner = PrepositionPursuitLearner(
        learning_factor=0.5,
        graph_match_confirmation_threshold=0.7,
        lexicon_entry_threshold=0.7,
        rng=rng,
        smoothing_parameter=0.001,
        ontology=GAILA_PHASE_1_ONTOLOGY,
    )  # type: ignore
    ball = standard_object("ball", BALL)
    table = standard_object("table", TABLE)
    on_train_curriculum = phase1_instances(
        "Preposition Unit Train",
        situations=sampled(
            _on_template(ball, table, immutableset(), is_training=True),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=10,
        ),
    )
    on_test_curriculum = phase1_instances(
        "Preposition Unit Test",
        situations=sampled(
            _on_template(ball, table, immutableset(), is_training=False),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
    )

    # Set up object recognizer, given the two objects we 'already' recognize
    object_recognizer = ObjectRecognizer(
        {
            node.handle: PerceptionGraphPattern.from_schema(
                first(GAILA_PHASE_1_ONTOLOGY.structural_schemata(node))
            )
            for node in [BALL, TABLE]
        }
    )

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in on_train_curriculum.instances():
        # Get the object matches first - preposition learner can't learn without already recognized objects
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            object_recognizer=object_recognizer,
        )

    for (
        _,
        test_lingustics_description,
        test_perceptual_representation,
    ) in on_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, object_recognizer
        )
        gold = test_lingustics_description.as_token_sequence()
        assert descriptions_from_learner
        assert [desc.as_token_sequence() for desc in descriptions_from_learner][0] == gold


def test_subset_preposition_beside_learner():
    rng = random.Random()
    rng.seed(0)
    learner = PrepositionPursuitLearner(
        learning_factor=0.5,
        graph_match_confirmation_threshold=0.7,
        lexicon_entry_threshold=0.7,
        rng=rng,
        smoothing_parameter=0.001,
        ontology=GAILA_PHASE_1_ONTOLOGY,
    )  # type: ignore
    ball = standard_object("ball", BALL)
    table = standard_object("table", TABLE)
    beside_train_curriculum = phase1_instances(
        "Preposition Beside Unit Train",
        situations=sampled(
            _beside_template(
                ball, table, immutableset(), is_training=True, is_right=True
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=10,
        ),
    )
    beside_test_curriculum = phase1_instances(
        "Preposition Beside Unit Test",
        situations=sampled(
            _beside_template(
                ball, table, immutableset(), is_training=False, is_right=True
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
    )

    # Set up object recognizer, given the two objects we 'already' recognize
    object_recognizer = ObjectRecognizer(
        {
            node.handle: PerceptionGraphPattern.from_schema(
                first(GAILA_PHASE_1_ONTOLOGY.structural_schemata(node))
            )
            for node in [BALL, TABLE]
        }
    )

    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in beside_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            object_recognizer=object_recognizer,
        )

    for (
        _,
        test_linguistic_description,
        test_perceptual_representation,
    ) in beside_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, object_recognizer
        )
        gold = test_linguistic_description.as_token_sequence()
        assert descriptions_from_learner
        assert [desc.as_token_sequence() for desc in descriptions_from_learner][0] == gold


def test_subset_preposition_under_learner():
    rng = random.Random()
    rng.seed(0)
    learner = PrepositionPursuitLearner(
        learning_factor=0.5,
        graph_match_confirmation_threshold=0.7,
        lexicon_entry_threshold=0.7,
        rng=rng,
        smoothing_parameter=0.001,
        ontology=GAILA_PHASE_1_ONTOLOGY,
    )  # type: ignore
    ball = standard_object("ball", BALL)
    table = standard_object("table", TABLE)
    under_train_curriculum = phase1_instances(
        "Preposition Under Unit Train",
        situations=sampled(
            _under_template(
                ball, table, immutableset(), is_training=True, is_distal=True
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=10,
        ),
    )
    under_test_curriculum = phase1_instances(
        "Preposition Under Unit Test",
        situations=sampled(
            _under_template(
                ball, table, immutableset(), is_training=False, is_distal=True
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
    )
    # Set up object recognizer, given the two objects we 'already' recognize
    object_recognizer = ObjectRecognizer(
        {
            node.handle: PerceptionGraphPattern.from_schema(
                first(GAILA_PHASE_1_ONTOLOGY.structural_schemata(node))
            )
            for node in [BALL, TABLE]
        }
    )
    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in under_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            object_recognizer=object_recognizer,
        )

    for (
        _,
        test_linguistic_description,
        test_perceptual_representation,
    ) in under_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, object_recognizer=object_recognizer
        )
        gold = test_linguistic_description.as_token_sequence()
        assert descriptions_from_learner
        assert [desc.as_token_sequence() for desc in descriptions_from_learner][0] == gold


def test_subset_preposition_over_learner():
    rng = random.Random()
    rng.seed(0)
    learner = PrepositionPursuitLearner(
        learning_factor=0.5,
        graph_match_confirmation_threshold=0.7,
        lexicon_entry_threshold=0.7,
        rng=rng,
        smoothing_parameter=0.001,
        ontology=GAILA_PHASE_1_ONTOLOGY,
    )  # type: ignore
    ball = standard_object("ball", BALL)
    table = standard_object("table", TABLE)
    over_train_curriculum = phase1_instances(
        "Preposition Over Unit Train",
        situations=sampled(
            _over_template(ball, table, immutableset(), is_training=True, is_distal=True),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=10,
        ),
    )
    over_test_curriculum = phase1_instances(
        "Preposition Over Unit Test",
        situations=sampled(
            _over_template(
                ball, table, immutableset(), is_training=False, is_distal=True
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
    )
    # Set up object recognizer, given the two objects we 'already' recognize
    object_recognizer = ObjectRecognizer(
        {
            node.handle: PerceptionGraphPattern.from_schema(
                first(GAILA_PHASE_1_ONTOLOGY.structural_schemata(node))
            )
            for node in [BALL, TABLE]
        }
    )
    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in over_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            object_recognizer=object_recognizer,
        )

    for (
        _,
        test_linguistic_description,
        test_perceptual_representation,
    ) in over_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, object_recognizer=object_recognizer
        )
        gold = test_linguistic_description.as_token_sequence()
        assert descriptions_from_learner
        assert [desc.as_token_sequence() for desc in descriptions_from_learner][0] == gold


# See https://github.com/isi-vista/adam/issues/422
@pytest.mark.skip(msg="In Preposition Test Temporarily Disabled")
def test_subset_preposition_in_learner():
    rng = random.Random()
    rng.seed(0)
    learner = PrepositionPursuitLearner(
        learning_factor=0.5,
        graph_match_confirmation_threshold=0.7,
        lexicon_entry_threshold=0.7,
        rng=rng,
        smoothing_parameter=0.001,
        ontology=GAILA_PHASE_1_ONTOLOGY,
    )  # type: ignore
    water = object_variable("water", WATER)
    cup = standard_object("cup", CUP)
    in_train_curriculum = phase1_instances(
        "Preposition In Unit Train",
        situations=sampled(
            _in_template(water, cup, immutableset(), is_training=True),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=10,
        ),
    )
    in_test_curriculum = phase1_instances(
        "Preposition In Unit Test",
        situations=sampled(
            _in_template(water, cup, immutableset(), is_training=False),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
    )
    # Set up object recognizer, given the two objects we 'already' recognize
    object_recognizer = ObjectRecognizer(
        {
            node.handle: PerceptionGraphPattern.from_schema(
                first(GAILA_PHASE_1_ONTOLOGY.structural_schemata(node))
            )
            for node in [WATER, CUP]
        }
    )
    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in in_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            object_recognizer=object_recognizer,
        )

    for (
        _,
        test_linguistic_description,
        test_perceptual_representation,
    ) in in_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, object_recognizer=object_recognizer
        )
        gold = test_linguistic_description.as_token_sequence()
        assert descriptions_from_learner
        assert [desc.as_token_sequence() for desc in descriptions_from_learner][0] == gold


def test_subset_preposition_behind_learner():
    rng = random.Random()
    rng.seed(0)
    learner = PrepositionPursuitLearner(
        learning_factor=0.5,
        graph_match_confirmation_threshold=0.7,
        lexicon_entry_threshold=0.7,
        rng=rng,
        smoothing_parameter=0.001,
        ontology=GAILA_PHASE_1_ONTOLOGY,
    )  # type: ignore
    ball = standard_object("ball", BALL)
    table = standard_object("table", TABLE)
    learner_object = standard_object("learner", LEARNER, added_properties=[IS_ADDRESSEE])
    mom = standard_object("mom", MOM, added_properties=[IS_SPEAKER])
    behind_train_curriculum = phase1_instances(
        "Preposition Behind Unit Train",
        situations=sampled(
            _behind_template(
                ball,
                table,
                immutableset([learner_object, mom]),
                is_training=True,
                is_near=True,
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=10,
        ),
    )
    behind_test_curriculum = phase1_instances(
        "Preposition Behind Unit Test",
        situations=sampled(
            _behind_template(
                ball,
                table,
                immutableset([learner_object, mom]),
                is_training=False,
                is_near=True,
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
    )
    # Set up object recognizer, given the two objects we 'already' recognize
    object_recognizer = ObjectRecognizer(
        {
            node.handle: PerceptionGraphPattern.from_schema(
                first(GAILA_PHASE_1_ONTOLOGY.structural_schemata(node))
            )
            for node in [BALL, TABLE]
        }
    )
    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in behind_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            object_recognizer=object_recognizer,
        )

    for (
        _,
        test_linguistic_description,
        test_perceptual_representation,
    ) in behind_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, object_recognizer=object_recognizer
        )
        gold = test_linguistic_description.as_token_sequence()
        assert descriptions_from_learner
        assert [desc.as_token_sequence() for desc in descriptions_from_learner][0] == gold


def test_subset_preposition_in_front_learner():
    rng = random.Random()
    rng.seed(0)
    learner = PrepositionPursuitLearner(
        learning_factor=0.5,
        graph_match_confirmation_threshold=0.7,
        lexicon_entry_threshold=0.7,
        rng=rng,
        smoothing_parameter=0.001,
        ontology=GAILA_PHASE_1_ONTOLOGY,
    )  # type: ignore
    ball = standard_object("ball", BALL)
    table = standard_object("table", TABLE)
    learner_object = standard_object("learner", LEARNER, added_properties=[IS_ADDRESSEE])
    mom = standard_object("mom", MOM, added_properties=[IS_SPEAKER])
    in_front_train_curriculum = phase1_instances(
        "Preposition In Front Unit Train",
        situations=sampled(
            _in_front_template(
                ball,
                table,
                immutableset([learner_object, mom]),
                is_training=True,
                is_near=True,
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=10,
        ),
    )
    in_front_test_curriculum = phase1_instances(
        "Preposition In Front Unit Test",
        situations=sampled(
            _in_front_template(
                ball,
                table,
                immutableset([learner_object, mom]),
                is_training=False,
                is_near=True,
            ),
            chooser=PHASE1_CHOOSER,
            ontology=GAILA_PHASE_1_ONTOLOGY,
            max_to_sample=1,
        ),
    )
    # Set up object recognizer, given the two objects we 'already' recognize
    object_recognizer = ObjectRecognizer(
        {
            node.handle: PerceptionGraphPattern.from_schema(
                first(GAILA_PHASE_1_ONTOLOGY.structural_schemata(node))
            )
            for node in [BALL, TABLE]
        }
    )
    for (
        _,
        linguistic_description,
        perceptual_representation,
    ) in in_front_train_curriculum.instances():
        learner.observe(
            LearningExample(perceptual_representation, linguistic_description),
            object_recognizer=object_recognizer,
        )

    for (
        _,
        test_linguistic_description,
        test_perceptual_representation,
    ) in in_front_test_curriculum.instances():
        descriptions_from_learner = learner.describe(
            test_perceptual_representation, object_recognizer=object_recognizer
        )
        gold = test_linguistic_description.as_token_sequence()
        assert descriptions_from_learner
        assert [desc.as_token_sequence() for desc in descriptions_from_learner][0] == gold