"""Event module."""

import re
from collections import UserDict, UserList

import numpy as np


def date(numpy_datetime64) -> str:
    """Extract date from numpy.datetime64 as a string."""
    return 'NaT' if np.isnat(numpy_datetime64) else str(numpy_datetime64.item().date())


TIMEDELTA = re.compile(
    r'(?P<value>\d+)\s?(?P<unit>millisecond|month|ms|[smhHdDMyY])s?'
)

NP_TIMEDELTA_UNITS = {
    'millisecond': 'ms',
    'H': 'h',
    'd': 'D',
    'month': 'M',
    'y': 'Y',
}


def timedelta(step):
    """Parse step as numpy.timedelta64 object.

    The value must be a `int` followed by an optional
    space and a valid unit.

    Examples of valid units:

        - ms, msec, millisecond
        - s, sec, second
        - m, min, minute
        - h, hour
        - D, day
        - M, month
        - Y, year

    Parameters
    ----------
    step: str
        Step to parse.

    Returns
    -------
    numpy.timedelta64
        Parsed numpy.timedelta64 step.

    Raises
    ------
    ValueError
        If the provided step format or unit is invalid.

    """
    if isinstance(step, np.timedelta64):
        return step

    match = TIMEDELTA.match(step)

    if not match:
        raise ValueError(f'Invalid step format: `{step}`')

    value, unit = match.group('value', 'unit')
    return np.timedelta64(int(value), NP_TIMEDELTA_UNITS.get(unit, unit))


class AbstractEvent(UserDict):
    """Single time event object."""
    def __init__(self, key, *args, **kwargs):
        self.key = key

        if 'contextual info' in kwargs:
            infos = kwargs.pop('contextual info')
            if infos:
                for info in infos.split(';'):
                    key, value = info.split('=', 1)
                    kwargs[key.strip()] = value.strip()

        super().__init__(*args, **kwargs)

        if 't_start' in self and 't_end' in self:
            self.__class__ = EventWindow

        elif 'event time [utc]' in self:
            self.__class__ = Event

        else:
            raise ValueError(f'Event time was not found: {kwargs}')

    def __repr__(self):
        return '\n - '.join([
            f'<{self.__class__.__name__}> {self}:',
            *[f'{k}: {v}' for k, v in self.items()]
        ])

    def __contains__(self, utc):
        if isinstance(utc, str) and utc in self.data:
            return True

        try:
            return self.contains(utc).any()
        except ValueError:
            return False

    def __add__(self, other):
        """Add to stop time."""
        return self.stop + timedelta(other)

    def __sub__(self, other):
        """Substract from start time."""
        return self.start - timedelta(other)

    @property
    def start(self):
        """Event start time."""
        raise NotImplementedError

    @property
    def stop(self):
        """Event stop time."""
        raise NotImplementedError

    def contains(self, pts):
        """Check if points are inside the temporal windows.

        Parameters
        ----------
        pts: np.array
            List of temporal UTC point(s): ``utc`` or ``[utc_0, …]``.
            If an object with :py:attr:`utc` attribute/property is provided,
            the intersection will be performed on these points.

        Returns
        -------
        np.array
            Return ``TRUE`` if the point is inside the pixel corners, and
            ``FALSE`` overwise.

        Note
        ----
        If the point is on the edge of the window it will be included.

        """
        if hasattr(pts, 'utc'):
            return self.contains(pts.utc)

        if isinstance(pts, str):
            return self.contains(np.datetime64(pts))

        if isinstance(pts, (list, tuple)):
            return self.contains(np.array(pts).astype('datetime64'))

        return (self.start <= pts) & (pts <= self.stop)


class Event(AbstractEvent):
    """Single time event object."""

    def __str__(self):
        return f'{self.key} ({date(self.start)})'

    @property
    def start(self):
        """Event start time."""
        return np.datetime64(self['event time [utc]'].replace('Z', ''))

    @property
    def stop(self):
        """Event stop time (same as start time)."""
        return self.start


class EventWindow(AbstractEvent):
    """Window time event object."""

    def __str__(self):
        return f'{self.key} ({date(self.start)} -> {date(self.stop)})'

    @property
    def start(self):
        """Event start time."""
        return np.datetime64(self['t_start'].replace('Z', ''))

    @property
    def stop(self):
        """Event stop time."""
        return np.datetime64(self['t_end'].replace('Z', ''))


class EventsList(UserList):
    """Collection of events."""
    def __str__(self):
        return (
            f'{self[0].key} '  # pylint: disable=no-member
            f'({date(self.start)} -> {date(self.stop)} | {len(self)} events)'
        )

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __getitem__(self, item):
        """Items can be queried by index or flyby crema name."""
        if isinstance(item, str):
            keys = self.crema_names
            if item not in keys:
                raise KeyError(f'Unknown flyby: `{item}`')
            return self[keys.index(item)]

        return self.data[item]

    def __contains__(self, utc):
        return self.contains(utc).any()

    @property
    def starts(self):
        """Event start times."""
        return [event.start for event in self]

    @property
    def stops(self):
        """Event stop times."""
        return [event.stop for event in self]

    @property
    def windows(self):
        """Event windows."""
        return [(event.start, event.stop) for event in self]

    @property
    def start(self):
        """Global events start time."""
        return min(self.starts)

    @property
    def stop(self):
        """Global events stop time."""
        return max(self.stops)

    @property
    def crema_names(self):
        """Crema names when present in contextual info field."""
        return [item.get('Crema name') for item in self]

    def contains(self, pts):
        """Check if points are inside any temporal window.

        Parameters
        ----------
        pts: np.array
            List of temporal UTC point(s): ``utc`` or ``[utc_0, …]``.
            If an object with :py:attr:`utc` attribute/property is provided,
            the intersection will be performed on these points.

        Returns
        -------
        np.array
            Return ``TRUE`` if the point is inside the pixel corners, and
            ``FALSE`` overwise.

        Note
        ----
        If the point is on the edge of the window it will be included.

        """
        return np.any([event.contains(pts) for event in self], axis=0)
