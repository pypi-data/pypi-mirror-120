import nuke


def funk(method, submitter, *args):
    """
    Create a function call as a string, passing the submitter and args.

    Useful for formatting the function argument to nuke.PyScript_Knob()

    examples:
    Given, s = nuke.toNode("Conductor")

    funk("a.b.c.d", s, 1, "foo")
    Result: s=nuke.toNode("Conductor");a.b.c.d(s, 1, 'foo')

    funk("d", s)
    Result: s=nuke.toNode("Conductor");d(s)

    """
    args = ", ".join(["s"] + [a.__repr__() for a in args])
    return f's=nuke.toNode("{submitter.name()}");{method}({args})'


def divider(submitter, name):
    """
    UI horizontal rule.
    """
    k = nuke.Text_Knob(name, "", "")
    submitter.addKnob(k)
