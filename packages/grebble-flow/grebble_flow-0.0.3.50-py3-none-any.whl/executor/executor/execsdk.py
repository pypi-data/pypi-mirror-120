def exec_code(code, session):
    the_code = (
        """
def factorial(session):
    """
        + code
        + """
return_me = factorial(session)
"""
    )
    loc = {}
    exec(the_code, {"session": session}, loc)
    return_workaround = loc["return_me"]
    return return_workaround
