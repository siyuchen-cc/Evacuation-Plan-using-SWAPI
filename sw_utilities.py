import copy
import csv
import json
import requests


class CustomEncoder(json.JSONEncoder):
    """WARNING: DO NOT MODIFY.

    Extends the json module's JSONEncoder class in order to serialize
    composite class instances.

     Note: include the pylint disable comment as Windows users have
     reported issues when the default() method is called.

     Methods:
        default: overrides default method
     """

    def default(self, obj): # pylint: disable=E0202
        """Check object is provisioned with a jsonable method that is
        callable. If yes override default serialization handling.

        Parameters:
            obj (object): class instance

        Returns:
            dict: dictionary representation of the object
        """

        if hasattr(obj, 'jsonable') and callable(obj.jsonable):
            return obj.jsonable()
        else:
            return json.JSONEncoder.default(self, obj)


def combine_data(default_data, override_data):
    """Create a deep copy of the default dictionary then update the copy with
    a second 'override' dictionary. A deep copy constructs a new compound object
    and then, recursively, inserts copies (rather than references) into it of the
    objects found in the original.

    Parameters:
        default_data (dict): key-value pairs that provide a collection of default values.
        override_data (dict): key-value pairs that are intended to override default values
                              and/or add new key-value pairs.

    Returns:
        dict: dictionary with updated key-value pairs.
    """

    data = copy.deepcopy(default_data)
    data.update(override_data)

    return data


def convert_str_to_float(value):
    """Attempts to convert a string to a float. If unsuccessful returns
    the value unchanged. Note that this function will return True for
    boolean values, faux string boolean values (e.g., "true"), "NaN",
    exponential notation, etc.
    Parameters:
        value (str): string to be converted.

    Returns:
        float: if string successfully converted else returns value as is
    """

    try:
        return float(value)
    except:
        return value


def convert_str_to_int(value):
    """Attempts to convert a string to an int. If unsuccessful returns
    the value unchanged. Note that this function will return True for
    boolean values, faux string boolean values (e.g., "true"), "NaN",
    exponential notation, etc.
    Parameters:
        value (str): string to be converted.

    Returns:
        int: if string successfully converted else returns value as is.
    """

    try:
        return int(value)
    except:
        return value


def convert_str_to_list(value, delimiter):
    """
    Splits a string using the provided delimiter.

    Parameters:
        value (str): string to be split.
        delimiter (str): delimiter used to split the string.

    Returns:
         list: a string converted to a list.

    """

    try:
        return value.split(delimiter)
    except:
        return value


def get_swapi_resource(url, params=None, timeout=20):
    """
    This function initiates an HTTP GET request to the SWAPI service in order to return a
    representation of a resource.

    Parameters:
        url (str): a url that specifies the resource.
        params (dict): optional dictionary of querystring arguments. The default value is None.
        timeout (int): timeout value in seconds. The default value is 5

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    if params:
        response = requests.get(url,params)
        dict = response.json()

    else:
        response = requests.get(url)
        dict = response.json()
        
    return dict


def is_unknown(value):
    """Performs a membership test for string values that equal 'unknown'
    or 'n/a'. Returns True if a match is obtained.

    Parameters:
        value (str): string to be evaluated

    Returns:
        bool: returns True if string match is obtained
    """
    unknown_values = ('n/a','unknown')
    if value.lower().strip() in unknown_values:
        return True
    else:
        return False


def read_csv_as_dict(path, delimiter=','):
    """Accepts a path, creates a file object, and returns a list of
    dictionaries that represent the row values.

    Parameters:
        path (str): path to file
        delimiter (str): delimiter that overrides the default delimiter

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(path, 'r', newline='', encoding='utf-8') as csv_file:
        data = []
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        for line in reader:
            data.append(dict(line)) # OrderedDict()
            # data.append(dict(line)) # convert OrderedDict() to dict

        return data


def read_json(filepath):
    """
    This function reads a JSON document and returns a dictionary if provided with a valid
    filepath.

    Parameters:
        filepath (str): path to file.

    Returns:
        data: dictionary representations of the decoded JSON document.
    """

    with open(filepath, 'r', encoding='utf-8') as file_obj:
        data = json.load(file_obj)

    return data


def write_custom_json(filepath, obj):
    """Serializes complex objects (e.g., composite class instances) as JSON
    by adding a CustomEncoder to the json.dump() call. Writes content to the
    provided filepath.

    Parameters:
        filepath (str): the path to the file.
        data (dict): the data to be encoded as JSON and written to the file.

    Returns:
        None
    """

    with open(filepath, 'w', encoding='utf-8') as file_obj:
        json.dump(obj, file_obj, cls=CustomEncoder, ensure_ascii=False, indent=2)
