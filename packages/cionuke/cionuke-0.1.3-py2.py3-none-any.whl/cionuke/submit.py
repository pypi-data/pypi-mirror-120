"""
Handle the submission.
"""

from contextlib import contextmanager
import nuke
from ciocore import conductor_submit

from cionuke.components import (
    project,
    title,
    instance_type,
    software,
    environment,
    metadata,
    assets,
    frames,
    advanced,
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
)


@contextmanager
def create_directories_on(submitter):
    """
    Turn on create_directoiries on write nodes for the submission.
    """
    write_nodes = [n for n in submitter.dependencies() if n.Class() == "Write"]
    orig_states = [w.knob("create_directories").value() for w in write_nodes]
    zipped = zip(write_nodes, orig_states)
    try:
        for pair in zipped:
            pair[0].knob("create_directories").setValue(1)
        yield
    finally:
        for pair in zipped:
            pair[0].knob("create_directories").setValue(pair[1])


@contextmanager
def transient_save(submitter):
    """
    Save with the autosave name for submission, then revert.
    """
    cio_filename = submitter.knob("cio_autosave_template").evaluate()
    try:
        original = nuke.Root().knob("name").getValue()
        nuke.scriptSaveAs(cio_filename, overwrite=1)
        yield
    except OSError:
        print("Problem saving nuke script")
    finally:
        nuke.Root().knob("name").setValue(original)


def submit(submitter):
    """
    Save or autosave, then submit

    Returns:
        tuple: submission response and code.
    """
    do_autosave = bool(submitter.knob("cio_do_autosave").getValue())
    if do_autosave:
        with transient_save(submitter):
            with create_directories_on(submitter):
                return do_submission(submitter)

    with create_directories_on(submitter):
        if nuke.Root().modified():
            if not nuke.scriptSave():
                print("Cancelled")
                return
        return do_submission(submitter)


def do_submission(submitter):
    """
    Do submission.

    Returns:
        tuple: submission response and code.
    """
    kwargs = {"should_scrape_assets": True}
    submission = resolve_submission(submitter, **kwargs)
    remote_job = conductor_submit.Submit(submission)
    return remote_job.main()


def resolve_submission(submitter, **kwargs):
    """
    Compile submission payload from all components.

    Returns:
        dict: payload, including tasks, assets, project, and so on
    """
    submission = {}

    for component in COMPONENTS:
        submission.update(component.resolve(submitter, **kwargs))
    return submission
