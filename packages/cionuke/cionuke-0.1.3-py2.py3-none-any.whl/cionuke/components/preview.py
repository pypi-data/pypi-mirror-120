import nuke

from cionuke import utils, submit

from PySide2 import QtWidgets, QtGui
import json

from cionuke.components.conductor_knob import ConductorKnob

AFFECTOR_KNOBS = [c for component in submit.COMPONENTS for c in component.affector_knobs()]
AFFECTOR_KNOBS.extend(["cio_show_assets", "cio_update_preview"])

def knobChanged(node, knob):
    """Respond to settings changes.
    
    knob may be a knob or the name of a knob
    """
 
    if knob.name() not in AFFECTOR_KNOBS:
        return

    kwargs = {"should_scrape_assets": knob.name() == "cio_show_assets"}

    submission = submit.resolve_submission(node, **kwargs)
 
    payload = json.dumps(submission, indent=2)
    node.knob("cio_preview").setValue(payload)

    if node.knob("cio_preview_ui").getObject():
        node.knob("cio_preview_ui").getObject().updateValue()

class PreviewKnob(ConductorKnob):
    def __init__(self, submitter):
        super(PreviewKnob, self).__init__(submitter)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(1)

        self.content_layout.addWidget(scroll_area)

        self.component = QtWidgets.QTextEdit()
        self.component.setReadOnly(True)
        self.component.setWordWrapMode(QtGui.QTextOption.NoWrap)
        scroll_area.setWidget(self.component)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def updateValue(self):
        """
        Populate the UI from the hidden storage knob.

        Called automatically by Nuke when needed. The storage knob is updated when upsteam knobs
        change.
        """
        print("PreviewKnob updateValue")
        try:
            self.component.setText(self.submitter.knob("cio_preview").getText())
        except ValueError as ex:
            self.component.setText(str(ex))


def build(submitter):
    """
    Build custom UI knob and a string knob for storage.

    The storage knob contains JSON.
    """

    knob = nuke.PyScript_Knob("cio_update_preview", "Update")
    submitter.addKnob(knob)

    knob = nuke.PyScript_Knob("cio_show_assets", "Update with Assets")
    submitter.addKnob(knob)


    knob = nuke.String_Knob("cio_preview", "Preview Raw", "")
    submitter.addKnob(knob)
    knob.setVisible(False)

    cmd = "preview.PreviewKnob(nuke.thisNode())"
    knob = nuke.PyCustom_Knob("cio_preview_ui", "", cmd)
    knob.setFlag(nuke.STARTLINE)
    submitter.addKnob(knob)

