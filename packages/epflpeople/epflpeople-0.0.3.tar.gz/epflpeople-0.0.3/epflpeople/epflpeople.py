import requests

SEARCH_URL = 'https://search.epfl.ch/json/ws_search.action'
PHOTO_URL = 'https://people.epfl.ch/private/common/photos/links/'

PP_PRINT = [
    'firstname',
    'name',
    'position',
    'unit',
    'sciper',
    'email',
    'homepage',
    'guest',
    'unitPath',
]
ACCREDS = 'accreds'
PP_PRINT_ACCREDS = [
    'acronym',
    'name',
    'position',
    'office',
    'status',
    'homepage',
    'address',
    'phones',
    'officeList',
    'phoneList',
]


def find_by_sciper(sciper, locale='en'):
    """
    Find a person's info from the given sciper
    :param sciper: Sciper number of the person
    :param locale: response in english ('en') or in french ('fr')
    :return: Person info if the person is found else an error string explaining the problem
    """
    if not __is_sciper(sciper):
        return 'Expected sciper number but found ' + repr(sciper)
    payload = {'q': sciper, 'request_locale': locale}

    response = requests.get(SEARCH_URL, params=payload)
    '''
    ["accreds", "email", "firstname", "guest", "homePage", "name", "position", "profile", "sciper", "unit", "unitPath"]
    '''
    if response.status_code == requests.codes.ok:
        if len(response.text) > 2:
            return response.json()
        else:
            return 'This person does not exist'
    else:
        return 'External service not responding'


def find(search, locale='en'):
    """
    Find a person using any general criteria (email, sciper, name, surname, etc ...)
    :param search: a string to search a person
    :param locale: response in english ('en') or in french ('fr')
    :return: Person info if the person is found else an error string explaining the problem
    """
    payload = {'q': search, 'request_locale': locale}

    response = requests.get(SEARCH_URL, params=payload)

    if response.status_code == requests.codes.ok:
        if len(response.text) > 2:  # not an empty array
            return response.json()
        else:
            return 'This person does not exist'
    else:
        return 'External service not responding'


def has_photo(sciper):
    """
    Search if a person has a public photo
    :param sciper: sciper from person
    :return: Photo url if found else None
    """
    url = PHOTO_URL + str(sciper) + '.jpg'
    response = requests.get(url, stream=True)

    if response.status_code == requests.codes.ok:
        return url
    else:  # 404
        return None


def __is_sciper(sciper):
    """
    Checks if the given argument is a valid Sciper number
    :param sciper: sciper to check
    :return: Whether sciper is valid or not
    """
    if str(sciper).isnumeric():
        sciper = int(sciper)
        if 100000 < sciper < 999999:
            return True
    return False


def find_first(search, format_output=False, **kwargs):
    res = find(search, **kwargs)[0]
    if format_output:
        return pretty_print(res)
    else:
        return res


def find_all(search, format_output=True, **kwargs):
    res = find(search, *kwargs)
    output = ''
    for i, r in enumerate(res):
        output += f'\n\n===== Result {i} =====\n'
        output += pretty_print(r)
    return output


def pretty_print(people: dict):
    output = '\n--- General info ---\n'
    output += '\n'.join(enumerate_properties(people, PP_PRINT)) + '\n'
    for i, accred in enumerate(people.get(ACCREDS)):
        output += f'\n--- Accred {i+1} ---\n'
        output += '\n'.join(enumerate_properties(accred, PP_PRINT_ACCREDS)) + '\n'
    return output


def enumerate_properties(obj, key_list):
    max_w = max([len(k) for k in key_list])
    for key in key_list:
        value = obj.get(key)
        if value:
            if isinstance(value, list):
                yield f'{key.capitalize().rjust(max_w)}: {", ".join(value)}'
                return
            if key == 'address':
                value = value.replace('$', '\n'+' '*(max_w+1))
            yield f'{key.capitalize().rjust(max_w)}: {value}'
