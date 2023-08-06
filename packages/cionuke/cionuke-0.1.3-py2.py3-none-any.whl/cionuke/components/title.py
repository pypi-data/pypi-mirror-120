import nuke


def build(submitter):
    """Build knobs to specify the job title."""
    k = nuke.EvalString_Knob("cio_title", "Job title", "NUKE [string trim [value root.name]]")
    submitter.addKnob(k)


def resolve(node, **kwargs):
    return {"job_title": node.knob("cio_title").evaluate()}


def affector_knobs():
    """Knobs will affect the payload when changed."""
    return ["cio_title"]
