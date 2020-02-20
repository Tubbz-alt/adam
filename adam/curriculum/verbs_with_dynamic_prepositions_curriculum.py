from itertools import chain
from typing import Iterable

from immutablecollections import immutableset
from more_itertools import flatten

from adam.axes import HorizontalAxisOfObject, FacingAddresseeAxis
from adam.curriculum.curriculum_utils import (
    standard_object,
    phase1_instances,
    PHASE1_CHOOSER,
    Phase1InstanceGroup,
    GROUND_OBJECT_TEMPLATE,
)
from adam.language_specific.english.english_language_generator import (
    USE_ADVERBIAL_PATH_MODIFIER,
)
from adam.ontology import THING
from adam.ontology.during import DuringAction
from adam.ontology.phase1_ontology import (
    AGENT,
    bigger_than,
    GOAL,
    GAILA_PHASE_1_ONTOLOGY,
    HOLLOW,
    SIT,
    ANIMATE,
    INANIMATE_OBJECT,
    CAN_HAVE_THINGS_RESTING_ON_THEM,
    SIT_THING_SAT_ON,
    CAN_BE_SAT_ON_BY_PEOPLE,
    THEME,
    THROW,
    THROW_GOAL,
    strictly_above,
    above,
    HAS_SPACE_UNDER,
    PERSON_CAN_HAVE,
    TRANSFER_OF_POSSESSION,
)
from adam.ontology.phase1_spatial_relations import (
    Region,
    Direction,
    INTERIOR,
    GRAVITATIONAL_UP,
    EXTERIOR_BUT_IN_CONTACT,
    PROXIMAL,
    DISTAL,
    TOWARD,
    SpatialPath,
)
from adam.situation import Action
from adam.situation.templates.phase1_templates import (
    TemplateObjectVariable,
    Phase1SituationTemplate,
    sampled,
    action_variable,
)

BOOL_SET = immutableset([True, False])


# THROW templates


def _throw_to_template(
    # "Mom throws a ball to a chair"
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-to-{goal_reference.handle}",
        salient_object_variables=[agent, theme, goal_reference],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[
                    (AGENT, agent),
                    (THEME, theme),
                    (GOAL, Region(goal_reference, distance=PROXIMAL)),
                ],
            )
        ],
        constraining_relations=[bigger_than(agent, theme)],
    )


def _throw_to_recipient_template(
    # "Mom throws a ball to a baby"
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    goal: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
    *,
    is_caught: bool,
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-to-recipient-{goal.handle}",
        salient_object_variables=[agent, theme, goal],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[(AGENT, agent), (THEME, theme), (GOAL, goal)]
                if is_caught
                else [
                    (AGENT, agent),
                    (THEME, theme),
                    (GOAL, Region(goal, distance=PROXIMAL)),
                ],
            )
        ],
        constraining_relations=[bigger_than(agent, theme), bigger_than(goal, theme)],
    )


def _throw_in_template(
    # "Dad throws a ball (and it lands) in a box"
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-in-{goal_reference.handle}",
        salient_object_variables=[agent, theme, goal_reference],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[
                    (AGENT, agent),
                    (THEME, theme),
                    (GOAL, Region(goal_reference, distance=INTERIOR)),
                ],
            )
        ],
        constraining_relations=[
            bigger_than(agent, theme),
            bigger_than(goal_reference, theme),
        ],
    )


def _throw_on_template(
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-on-{goal_reference.handle}",
        salient_object_variables=[agent, theme, goal_reference],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[
                    (AGENT, agent),
                    (THEME, theme),
                    (
                        GOAL,
                        Region(
                            goal_reference,
                            direction=GRAVITATIONAL_UP,
                            distance=EXTERIOR_BUT_IN_CONTACT,
                        ),
                    ),
                ],
            )
        ],
        constraining_relations=[bigger_than(agent, theme)],
    )


def _throw_beside_template(
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
    *,
    is_right: bool,
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-beside-{goal_reference.handle}",
        salient_object_variables=[agent, theme, goal_reference],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[
                    (AGENT, agent),
                    (THEME, theme),
                    (
                        GOAL,
                        Region(
                            goal_reference,
                            direction=Direction(
                                positive=is_right,
                                relative_to_axis=HorizontalAxisOfObject(
                                    goal_reference, index=0
                                ),
                            ),
                            distance=PROXIMAL,
                        ),
                    ),
                ],
            )
        ],
        constraining_relations=[bigger_than(agent, theme)],
    )


def _throw_in_front_of_behind_template(
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
    *,
    is_distal: bool,
    is_in_front: bool,
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-in-front-of-behind-{goal_reference.handle}",
        salient_object_variables=[agent, theme, goal_reference],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[
                    (AGENT, agent),
                    (THEME, theme),
                    (
                        GOAL,
                        Region(
                            goal_reference,
                            direction=Direction(
                                positive=is_in_front,
                                relative_to_axis=FacingAddresseeAxis(goal_reference),
                            ),
                            distance=DISTAL if is_distal else PROXIMAL,
                        ),
                    ),
                ],
            )
        ],
        constraining_relations=[bigger_than(agent, theme)],
    )


def _throw_under_template(
    # "A baby throws a cup under a table"
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
    *,
    is_distal: bool,
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-under-{goal_reference.handle}",
        salient_object_variables=[agent, theme, goal_reference],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[
                    (AGENT, agent),
                    (THEME, theme),
                    (
                        GOAL,
                        Region(
                            goal_reference,
                            direction=GRAVITATIONAL_UP,
                            distance=DISTAL if is_distal else PROXIMAL,
                        ),
                    ),
                ],
            )
        ],
        constraining_relations=[
            bigger_than(agent, theme),
            bigger_than(goal_reference, theme),
        ],
    )


def _throw_path_over_template(
    # "A baby throws a truck over a table (and lands on the other side)"
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    object_in_path: TemplateObjectVariable,
    implicit_goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-with-path-over-{object_in_path.handle}",
        salient_object_variables=[agent, theme, object_in_path],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[(AGENT, agent), (THEME, theme)],
                auxiliary_variable_bindings=[
                    (THROW_GOAL, Region(implicit_goal_reference, distance=PROXIMAL))
                ],
                during=DuringAction(
                    at_some_point=[strictly_above(theme, object_in_path)]
                ),
            )
        ],
        constraining_relations=[bigger_than(agent, theme)],
    )


def _throw_path_under_template(
    # "A baby throws a truck under a table (and lands on the other side)"
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    object_in_path: TemplateObjectVariable,
    implicit_goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
    *,
    is_distal: bool,
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-with-path-under-{object_in_path.handle}",
        salient_object_variables=[agent, theme, object_in_path],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[(AGENT, agent), (THEME, theme)],
                auxiliary_variable_bindings=[
                    (
                        THROW_GOAL,
                        Region(
                            implicit_goal_reference,
                            distance=DISTAL if is_distal else PROXIMAL,
                        ),
                    )
                ],
                during=DuringAction(
                    at_some_point=[strictly_above(object_in_path, theme)]
                ),
            )
        ],
        constraining_relations=[
            bigger_than(agent, theme),
            bigger_than(object_in_path, theme),
        ],
    )


def _throw_up_down_template(
    # Up: the thrown object goes above the thrower at some point
    # Down: the thrown object only travels downward
    agent: TemplateObjectVariable,
    theme: TemplateObjectVariable,
    implicit_goal_reference: TemplateObjectVariable,
    background: Iterable[TemplateObjectVariable],
    *,
    is_up: bool,
) -> Phase1SituationTemplate:
    return Phase1SituationTemplate(
        f"{agent.handle}-throws-{theme.handle}-up-down",
        salient_object_variables=[agent, theme],
        background_object_variables=background,
        actions=[
            Action(
                THROW,
                argument_roles_to_fillers=[(AGENT, agent), (THEME, theme)],
                auxiliary_variable_bindings=[
                    (THROW_GOAL, Region(implicit_goal_reference, distance=PROXIMAL))
                ],
                during=DuringAction(at_some_point=[above(theme, agent)])
                if is_up
                else DuringAction(
                    objects_to_paths=[
                        (
                            theme,
                            SpatialPath(TOWARD, reference_object=GROUND_OBJECT_TEMPLATE),
                        )
                    ]
                ),
            )
        ],
        constraining_relations=[bigger_than(agent, theme)],
        syntax_hints=[USE_ADVERBIAL_PATH_MODIFIER],
    )


def _make_throw_with_prepositions(
    num_samples: int = 5, *, noise_objects: int = 0
) -> Phase1InstanceGroup:
    agent = standard_object("agent", THING, required_properties=[ANIMATE])
    theme = standard_object("theme", INANIMATE_OBJECT)
    theme_can_have = standard_object(
        "theme_can_have", INANIMATE_OBJECT, required_properties=[PERSON_CAN_HAVE]
    )
    goal_reference = standard_object("goal_reference", THING)
    goal_catcher = standard_object("goal_catcher", THING, required_properties=[ANIMATE])
    goal_in = standard_object("goal_in", THING, required_properties=[HOLLOW])
    goal_on = standard_object(
        "goal_on", THING, required_properties=[CAN_HAVE_THINGS_RESTING_ON_THEM]
    )
    goal_under = standard_object(
        "goal_under", THING, required_properties=[HAS_SPACE_UNDER]
    )
    implicit_goal_reference = standard_object("goal_reference", THING)
    background = immutableset(
        standard_object(f"noise_object_{x}") for x in range(noise_objects)
    )
    situation_templates = [
        _throw_to_template(agent, theme, goal_reference, background),
        _throw_in_template(agent, theme, goal_in, background),
        _throw_on_template(agent, theme, goal_on, background),
    ]

    return phase1_instances(
        "Throw + PP",
        chain(
            # to, in, on
            flatten(
                [
                    sampled(
                        template,
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                    for template in situation_templates
                ]
            ),
            # to (expecting object to be caught)
            flatten(
                [
                    sampled(
                        _throw_to_recipient_template(
                            agent,
                            theme_can_have,
                            goal_catcher,
                            background,
                            is_caught=is_caught,
                        ),
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                    for is_caught in BOOL_SET
                ]
            ),
            # beside
            flatten(
                [
                    sampled(
                        _throw_beside_template(
                            agent, theme, goal_reference, background, is_right=is_right
                        ),
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                    for is_right in BOOL_SET
                ]
            ),
            # in front of, behind
            flatten(
                [
                    sampled(
                        _throw_in_front_of_behind_template(
                            agent,
                            theme,
                            goal_reference,
                            background,
                            is_distal=is_distal,
                            is_in_front=is_in_front,
                        ),
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                    for is_distal in BOOL_SET
                    for is_in_front in BOOL_SET
                ]
            ),
            # under
            flatten(
                [
                    sampled(
                        _throw_under_template(
                            agent, theme, goal_under, background, is_distal=is_distal
                        ),
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                    for is_distal in BOOL_SET
                ]
            ),
            # path over
            flatten(
                [
                    sampled(
                        _throw_path_over_template(
                            agent,
                            theme,
                            goal_reference,
                            implicit_goal_reference,
                            background,
                        ),
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                ]
            ),
            # path under
            flatten(
                [
                    sampled(
                        _throw_path_under_template(
                            agent,
                            theme,
                            goal_under,
                            implicit_goal_reference,
                            background,
                            is_distal=is_distal,
                        ),
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                    for is_distal in BOOL_SET
                ]
            ),
            # up, down
            flatten(
                [
                    sampled(
                        _throw_up_down_template(
                            agent, theme, goal_reference, background, is_up=is_up
                        ),
                        ontology=GAILA_PHASE_1_ONTOLOGY,
                        chooser=PHASE1_CHOOSER,
                        max_to_sample=num_samples,
                    )
                    for is_up in BOOL_SET
                ]
            ),
        ),
    )


def make_verb_with_dynamic_prepositions_curriculum(
    num_samples: int = 5, *, num_noise_objects: int = 0
):
    return [_make_throw_with_prepositions(num_samples, noise_objects=num_noise_objects)]
