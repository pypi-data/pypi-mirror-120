"""ESA API module."""

import json
from pathlib import Path
from urllib.request import HTTPError, urlopen, urlretrieve

from .vars import DATA
from ..misc import logger


API = 'https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos'
ESA_API_CACHE = {}

log_esa_api, debug_esa_api = logger('ESA API')


def esa_api(uri):
    """Retrieve the tags from ESA Cosmos Bitbucket repo.

    Parameters
    ----------
    uri: str
        Cosmos Bitbucket API entrypoint URI.

    Returns
    -------
    list
        List of tags.

    Raises
    ------
    IOError
        If the API URL is invalid (usually 404 error code).

    """
    if uri in ESA_API_CACHE:
        log_esa_api.debug('Use data from the cache: %s.', uri)
        return ESA_API_CACHE[uri]

    try:
        log_esa_api.debug('Downloading: %s', uri)

        with urlopen(f'{API}/{uri}') as resp:
            data = json.loads(resp.read())

        log_esa_api.debug('Data: %s', data)

    except HTTPError:
        raise IOError(f'Impossible to retrieve the tags from `{uri}`.') from None

    log_esa_api.debug('Saved the data in the cache.')
    ESA_API_CACHE[uri] = data

    return data


def get_tag(mission, version='latest', limit=25):
    """Get tag version(s) of the metakernels from ESA Cosmos repo.

    https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos/juice/tags

    Parameters
    ----------
    mission: str
        Mission name in the cosmos repo.
    version: str, optional
        Version short key or `latest` or `all` (default: 'latest').
    limit: int, optional
        Maximum number of tags if `all` is requested (default: 25).

    Returns
    -------
    str or list
        Long SKD version key(s).

    Raises
    ------
    AttributeError
        If the mission name provided is invalid.
    ValueError
        If the requested version was not found.

    Note
    ----
    If multiple version have the same short version key, only
    the most recent will be returned. If you want a specific version
    you need to be as precise as possible.

    """
    if not mission:
        raise AttributeError('The mission name must be defined.')

    if version.lower() == 'latest':
        log_esa_api.info('Get the latest tag for `%s`.', mission)
        uri = f'{mission.lower()}/tags?limit=1'

    elif version.lower() == 'all':
        log_esa_api.info('Get all the tags for `%s`.', mission)
        uri = f'{mission.lower()}/tags?limit={limit}'

    else:
        log_esa_api.info('Search for the tag closest to `%s` for `%s`.', version, mission)
        uri = f'{mission.lower()}/tags?filterText={version}'

    tags = [value.get('displayId') for value in esa_api(uri)['values']]

    if not tags:
        raise ValueError(f'Version `{version}` is not available.')

    return tags if version.lower() == 'all' else tags[0]


def get_mk(mission, mk='latest', version='latest'):
    """Get metakernel file(s) from ESA Cosmos repo for a given tag.

    https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos/juice/browse/kernels/mk/?at=refs/tags/v270_20201113_001
    https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos/juice/raw/kernels/mk/juice_crema_3_0.tm?at=refs/tags/v270_20201113_001

    Parameters
    ----------
    mission: str
        Mission name in the cosmos repo.
    mk: str, optional
        Metakernel name/shortcut to download.
        If `latest` is provided (default), the lastest metakernel will be selected.
        If `all` is provided, the function will search all the available metakernel(s)
        for the provided tag.
    version: str, optional
        Tagged version `latest` (default) or `all`.
        If the version provided is not fully defined, the API will be query
        to search for the closest version.
        If `all` is provided, the function will list all the available metakernel(s)
        for all the tags.

    Returns
    -------
    str or list
        Metakernel file name.

    Raises
    ------
    AttributeError
        If the mission name provided is invalid.
    ValueError
        If not metakernel was found for the requested arguments.
    FileNotFoundError
        If the file is not found on the cosmos repo.

    """
    if not mission:
        raise AttributeError('The mission name must be defined.')

    # Get one or all the metakernel(s) for al the available versions
    if version.lower() == 'all':
        return {
            v: get_mk(mission, mk='all', version=v)
            for v in get_tag(mission, version=version)
        }

    tag = get_tag(mission, version=version) if len(version) != 17 else version

    at = f'refs/tags/{tag}'

    # Get all the metakernel for a given version
    if mk.lower() in ['latest', 'all']:
        log_esa_api.info('Get all the metakernel at `%s`.', tag)
        uri = f'{mission.lower()}/browse/kernels/mk/?at={at}'

        mks = [
            mk_file
            for value in esa_api(uri)['children']['values']
            for mk_file in value['path']['components']
            if mk_file.endswith('.tm')
        ]

        if mk.lower() == 'all':
            return mks

        # Select only the latest metakernel for the selected tag.
        mk = mks[-1]

    # Get a single metakernel
    if not str(mk).endswith('.tm'):
        mk = f'{mission.lower()}_crema_{crema_ref(mk)}.tm'

    fname = DATA / mission.lower() / tag / str(mk)

    if not fname.exists():
        log_esa_api.info('Get %s at `%s`.', mk, tag)

        url = f'{API}/{mission.lower()}/raw/kernels/mk/{mk}?at={at}'

        try:
            log_esa_api.debug('Download mk at: %s.', url)
            fout, _ = urlretrieve(url)
        except HTTPError:
            raise FileNotFoundError(f'`{mk}` at `{tag}` does not exist.') from None

        fname.parent.mkdir(parents=True, exist_ok=True)
        Path(fout).rename(fname)

    return fname


def crema_ref(ref):
    """Get CReMA ref formatter."""
    crema = str(ref)

    # Replace with underscores
    for c in '.- ':
        crema = crema.replace(c, '_')

    # Special cases
    crema = crema.replace('(', '').replace('_only)', '')  # `(cruise only)` -> `cruise`

    return crema
