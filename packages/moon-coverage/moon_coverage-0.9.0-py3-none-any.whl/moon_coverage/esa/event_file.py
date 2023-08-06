"""ESA events files module."""

from ..events import Event, EventsFile, EventsList, EventWindow


class EsaMissionPhases(EventsFile):
    """ESA mission phases event file."""

    def __init__(self, fname):
        super().__init__(fname, primary_key='Name')


class EsaMissionTimeline(EventsFile):
    """ESA mission timeline event file."""

    def __init__(self, fname):
        super().__init__(fname, primary_key='Event Name')


class EsaMissionEvents(EventsFile, EventsList, EventWindow, Event):
    """Generic ESA mission events file.

    By default, a header is appended to the file with the
    following parameters:

    ``# name, t_start, t_end, subgroup, working_group``

    but you can provide your own or set it to ``None`` is
    the first row is already the header.

    The primary key is also initialized at ``'name'`` but you
    can use any other column.

    """

    def __new__(cls, fname,
                primary_key='name',
                header='# name, t_start, t_end, subgroup, working_group'):
        events = EventsFile(fname, primary_key=primary_key, header=header)

        # Convert the object if only 1 event is present
        if len(events) == 1:
            key = list(events.keys())[0]
            return events[key]

        return events
