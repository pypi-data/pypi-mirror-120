"""Entry point for the Submitter."""

import datetime
import os
import sys

import nuke

from cionuke import utils
from cionuke.components import (
    actions,
    advanced,
    autosave,
    environment,
    assets,
    frames,
    instance_type,
    metadata,
    preview,
    project,
    software,
    title,
)

COMPONENTS = (
    project,
    title,
    instance_type,
    software,
    environment,
    metadata,
    assets,
    frames,
    advanced,
    autosave,
    preview,
)

SAFE_KNOB_CHANGED = """
try:
    entry.knobChanged()
except NameError:
    pass
"""


def add_to_nodes():
    """
    Add a Conductor submitter node to the project.

    Connect selected Write nodes to the Group node and add Conductor controls.
    """

    nodes = [n for n in nuke.selectedNodes() if n.Class() == "Write"]

    if not nodes:
        print("Select at least one Write node.")
        return

    submitter = nuke.createNode("Group")
    submitter.setName("Conductor")

    for i, node in enumerate(nodes):
        submitter.setInput(i, node)
        node.knob("selected").setValue(False)

    submitter.knob("selected").setValue(True)

    build_tabs(submitter)

    nuke.show(submitter)
    submitter.knob("Configure").setFlag(0)


def build_tabs(submitter):
    """
    Add Conductor controls.


    Args:
        submitter (Group node): The submitter node
    """
    config_tab = nuke.Tab_Knob("Configure")
    submitter.addKnob(config_tab)

    actions.build(submitter)
    title.build(submitter)
    project.build(submitter)
    instance_type.build(submitter)
    utils.divider(submitter, "entry1")
    software.build(submitter)
    utils.divider(submitter, "entry2")
    frames.build(submitter)
    utils.divider(submitter, "entry3")
    advanced.build(submitter)
    environment.build(submitter)
    utils.divider(submitter, "entry4")
    assets.build(submitter)
    utils.divider(submitter, "entry5")
    metadata.build(submitter)
    utils.divider(submitter, "entry6")
    autosave.build(submitter)

    preview_tab = nuke.Tab_Knob("Preview")
    submitter.addKnob(preview_tab)
    preview.build(submitter)

    validate_tab = nuke.Tab_Knob("Validation")
    submitter.addKnob(validate_tab)

    # SAFE_KNOB_CHANGED calls entry.knobChanged() in a try block
    # because the node is present on the render node but the
    # Python module is not.
    submitter.knob("knobChanged").setValue(SAFE_KNOB_CHANGED)

    # Trigger a preview update now
    preview.knobChanged(submitter, submitter.knob("cio_title"))


def knobChanged():
    """
    Notify all component modules when a knob changes.
    """
    node = nuke.thisNode()
    knob = nuke.thisKnob()
    for component in COMPONENTS:
        try:
            component.knobChanged(node, knob)
        except AttributeError:
            pass
