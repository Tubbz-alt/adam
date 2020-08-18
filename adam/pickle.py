from adam.axis import GeonAxis
from adam.learner.object_recognizer import SHARED_WORLD_ITEMS
from adam.perception import ObjectPerception, GROUND_PERCEPTION, LEARNER_PERCEPTION
from pickle import Pickler, Unpickler


PERSISTENT_AXIS_TAG = "PersistentAxis"
PERSISTENT_OBJECT_PERCEPTION_TAG = "PersistentObjectPerception"


class AdamPickler(Pickler):
    """
    A pickler customized for ADAM's needs.

    This pickler implements persistence logic for things that there should only be one of, like the
    ground, or the "gravitational up/down" axis.
    """

    @staticmethod
    def persistent_id(obj):
        if isinstance(obj, GeonAxis):
            if obj in SHARED_WORLD_ITEMS:
                return PERSISTENT_AXIS_TAG, obj.debug_name
            else:
                return None
        elif isinstance(obj, ObjectPerception):
            if obj == GROUND_PERCEPTION or obj == LEARNER_PERCEPTION:
                return PERSISTENT_OBJECT_PERCEPTION_TAG, obj.debug_handle
            else:
                return None
        else:
            return None


class AdamUnpickler(Unpickler):
    """
    An unpickler customized for ADAM's needs.

    This pickler implements the loading of things that there should only be one of, like the ground,
    or the "gravitational up/down" axis.
    """

    @staticmethod
    def persistent_load(persistence_id):
        if not isinstance(persistence_id, tuple) or len(persistence_id) < 1:
            raise RuntimeError(
                "Got bad persistence ID {pid}; persistence ID must be a tuple of at least one item"
            )

        tag = persistence_id[0]
        if tag == PERSISTENT_AXIS_TAG:
            name = persistence_id[1]
            for axis in SHARED_WORLD_ITEMS:
                # Check that the item is an axis before just to make sure
                if isinstance(axis, GeonAxis) and axis.debug_name == name:
                    return axis
            raise RuntimeError(
                f"Axis persisted with name {name} but no such shared world item found!"
            )

        elif tag == PERSISTENT_OBJECT_PERCEPTION_TAG:
            name = persistence_id[1]
            if name == GROUND_PERCEPTION.debug_handle:
                return GROUND_PERCEPTION
            else:
                raise RuntimeError(
                    f"Object perception persisted with name {name} but no such object perception known!"
                )
        else:
            raise RuntimeError(f"Got unrecognized persistence ID {persistence_id}!")
