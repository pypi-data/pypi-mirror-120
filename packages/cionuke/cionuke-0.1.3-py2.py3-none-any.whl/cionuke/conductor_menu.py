"""
Build Conductor Menu.

This file is an extension of the user's ~/.nuke/menu.py and is read in using
execfile. (It doesn't work with import.) 
"""
# If you are reading this and know a better way to get it registered, please change it and PR.

from importlib import reload

import nuke

from cionuke import const as k
from cionuke import entry, submit, utils
from cionuke.components import (actions, advanced, autosave, conductor_knob,
                                environment, assets, frames,
                                instance_type, metadata, preview, project,
                                software, title)
from cionuke.widgets import key_value_grp

if k.FEATURE_DEV:
    print("Reloading")
    reload(utils)
    reload(conductor_knob)
    reload(key_value_grp)
    reload(environment)
    reload(metadata)
    reload(assets)
    reload(frames)
    reload(project)
    reload(title)
    reload(actions)
    reload(instance_type)
    reload(software)
    reload(entry)
    reload(advanced)
    reload(preview)
    reload(autosave)
    reload(submit)

def quick_node():
    """
    Dev mode reload

    Also removes Conductor node and creates a new one with all writes connected.
    """
    from importlib import reload

    from cionuke import conductor_menu, entry

    reload(conductor_menu)
    conductor_nodes = [n for n in nuke.allNodes("Group") if n.knob("cio_title")]
    for cn in conductor_nodes:
        nuke.delete(cn)

    for node in nuke.allNodes("Write"):
        node.setSelected(True)

    entry.add_to_nodes()


nuke.menu("Nuke").addCommand("Render/Render selected on Conductor", lambda: entry.add_to_nodes())

if k.FEATURE_DEV:
    nuke.menu("Nuke").addCommand("Render/CIO Dev Refresh and Create", lambda: quick_node())
