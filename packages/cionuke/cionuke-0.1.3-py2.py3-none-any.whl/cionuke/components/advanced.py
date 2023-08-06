"""
Controls that are beyond basic operation.
"""
import nuke
import re
from cionuke import utils
from cionuke import const as k

from ciopath.gpath_list import PathList

DEFAULT_TASK_TEMPLATE = 'nuke -V 2 [value cio_range_args] -X [python {",".join([n.name() for n in nuke.thisNode().dependencies(nuke.INPUTS | nuke.HIDDEN_INPUTS)])}] "[value root.name]"'

def build(submitter):
    """
    Build the controls.
    """
    knob = nuke.Boolean_Knob("cio_use_daemon", "Use upload daemon")
    submitter.addKnob(knob)
    knob.setValue(1)

    knob = nuke.String_Knob("cio_emails", "Email notifications", "you@vfxco.com,me@vfxco.com")
    submitter.addKnob(knob)
    knob.setEnabled(False)

    knob = nuke.Boolean_Knob("cio_use_emails", "Enable")
    knob.clearFlag(nuke.STARTLINE)
    submitter.addKnob(knob)
    knob.setValue(0)

    knob = nuke.Int_Knob("cio_retries", "Retries on preemption")
    knob.setValue(1)
    knob.setFlag(nuke.STARTLINE)
    submitter.addKnob(knob)

    nuke.knobDefault("Group.cio_task", DEFAULT_TASK_TEMPLATE)
    knob = nuke.EvalString_Knob("cio_task", "Task template")
    knob.setValue(DEFAULT_TASK_TEMPLATE)

    submitter.addKnob(knob)

    knob = nuke.String_Knob("cio_range_args", "Range args")
    submitter.addKnob(knob)
    knob.setVisible(False)

    knob = nuke.String_Knob("cio_location", "Location")
    submitter.addKnob(knob)


    if k.FEATURE_DEV:
        utils.divider(submitter, "advanced1")
        knob = nuke.Boolean_Knob("cio_use_fixtures", "Use fixtures")
        submitter.addKnob(knob)
        knob.setValue(0)

    utils.divider(submitter, "advanced2")


def knobChanged(node, knob):
    """
    Adjust the enabled/visible state of UI components in this component.
    """
    knob_name = knob.name()
    if knob_name == "cio_use_emails":
        node.knob("cio_emails").setEnabled(bool(knob.getValue()))



def resolve(submitter, **kwargs):
    """
    Resolve the part of the payload that is handled by this component.
    """
    result = {}
    result["autoretry_policy"] = {"preempted": {"max_retries": int(submitter.knob("cio_retries").getValue())}}
    result["local_upload"] = not submitter.knob("cio_use_daemon").getValue()

    location = submitter.knob("cio_location").getValue().strip()
    if location:
        result["location"] = location

    if submitter.knob("cio_use_emails").getValue():
        emails = list([_f for _f in re.split(r"[, ]+", submitter.knob("cio_emails").getValue()) if _f])
        if emails:
            result["notify"] = emails


    write_paths = [n.knob("file").evaluate() for n in submitter.dependencies() if n.Class() == "Write"]

    try:
        common_path = PathList(*write_paths).common_path()
        result["output_path"] = common_path.fslash()
    except BaseException:
        result["output_path"] = "Invalid output paths"
   
    return  result


def affector_knobs():
    """knobs that affect the payload."""
    return [
        "cio_use_daemon",
        "cio_emails",
        "cio_use_emails",
        "cio_retries",
        "cio_task",
        "cio_location"
    ]
