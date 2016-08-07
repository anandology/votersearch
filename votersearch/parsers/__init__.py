from . import KA, KL, GA

PARSERS = {
    "KA": KA.Parser(),
    "KL": KL.Parser(),
    "GA": GA.Parser()
}

def get_parser(state):
    return PARSERS.get(state)

def get_voter_details(state, district, voterid):
    """Returns the voter details of voterid.

    The state and district values will be used to identify the state
    election commission website and to submit the voter search form.
    """
    parser = get_parser(state)
    if parser is None:
        raise Exception("State %s is not yet supported." % state)
    return parser.get_voter_details(state, district, voterid)
