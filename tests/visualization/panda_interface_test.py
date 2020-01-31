from math import isclose
from pandac.PandaModules import ConfigVariableString  # pylint: disable=no-name-in-module

from adam.visualization.panda3d_interface import SituationVisualizer
from adam.visualization.utils import Shape

# sets the rendering engine to not run, as it can't be handled by CI system
ConfigVariableString("window-type", "none").setValue("none")

# This should be the only test to actually instantiate panda3d
def test_basic_3d_scene() -> None:
    app = SituationVisualizer()

    model_scales = app.get_model_scales()

    # test grabbing the scale of a model (cube should be 2x2x2)
    assert isclose(model_scales[Shape.SQUARE.name][0], 2, rel_tol=0.05)
    assert isclose(model_scales[Shape.SQUARE.name][1], 2, rel_tol=0.05)
    assert isclose(model_scales[Shape.SQUARE.name][2], 2, rel_tol=0.05)

    app.add_model(Shape.SQUARE, name="Square0", position=(1, 2, 2))
    app.add_model(Shape.RECTANGULAR, name="rect0", position=(2, 2, 2))
    try:
        app.add_model(Shape.IRREGULAR, name="irreg0", position=(4, 4, 4))
    except KeyError:
        pass
    oval = app.add_model(Shape.OVALISH, name="oval0", position=(5, 5, 5))
    app.add_model(
        Shape.CIRCULAR, name="sphere0", position=(7, 7, 7), color=None, parent=oval
    )

    app.print_scene_graph()

    dummy_node = app.add_dummy_node("dummy", (0, 0, 0))
    other_dummy_node = app.add_dummy_node(
        "second_dummy", position=(0, 0, 0), parent=dummy_node
    )

    print(other_dummy_node)

    # having test cover these functions s/t they are at least executed

    app.clear_scene()

    app.add_model(Shape.RECTANGULAR, name="rect", position=(-2, 2, 2))

    app.add_model(Shape.CIRCULAR, name="sphere", position=(0, 0, 8))

    app.add_model(Shape.OVALISH, name="oval", position=(4, 5, 2))

    app.add_dummy_node("dummy_node", (5, 5, 2), None, scale_multiplier=1.0)
