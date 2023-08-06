"""
Handle the submission.
"""

from contextlib import contextmanager
import nuke
from ciocore import conductor_submit
import traceback
from ciocore import config
import json

try:
    from urllib import parse
except ImportError:
    import urlparse as parse


from cionuke.components import (
    actions,
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
    actions,
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
    Submit and handle the response
    """
    ul_command = "conductor uploader"
    dl_command = "conductor downloader"

    loc = submitter.knob("cio_location").getValue().strip()
    if loc:
        ul_command += " --location {}".format(loc)
    use_daemon = submitter.knob("cio_use_daemon").getValue()
 
    try:
        resp = save_and_submit(submitter)
    except BaseException as ex:
        msg = traceback.format_exc()
        nuke.alert(msg)
        return

    if not resp:
        nuke.alert("Submission cancelled.")
        return

    response, response_code = resp

    cfg = config.config().config

    if response_code <= 201:

        success_uri = response["uri"].replace("jobs", "job")
        job_url = parse.urljoin(cfg["auth_url"], success_uri)
        job_id = success_uri.split("/")[-1]
        dl_command += " --job_id {}".format(job_id)

        msg = "Success\n"
        msg += f"Use this URL to monitor your Conductor job:\n{job_url}\n" 
        if use_daemon:
            msg += "IMPORTANT: You have 'Use Upload Daemon' selected. Please open a terminal and type: '{}'".format(ul_command)
 
        msg += "To download finished frames, either use the Companion app, or enter the following command in a terminal:\n '{}'".format(dl_command)
        nuke.message(msg)
        print(msg)
    else:
        msg = "Failed to submit - Code:{}\n".format(response_code)
        msg += "Error uploading. You most likely have an invalid project, or some files changed while submitting.\n"
        msg += json.dumps(response)
        nuke.alert(msg)
        print(msg)

def save_and_submit(submitter):
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
    else:
        with create_directories_on(submitter):
            if nuke.Root().modified():
                if not nuke.scriptSave():
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
