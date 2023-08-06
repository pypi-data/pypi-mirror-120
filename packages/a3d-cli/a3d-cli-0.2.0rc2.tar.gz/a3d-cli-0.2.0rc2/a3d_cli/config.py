import configparser
import json


class MyParser(configparser.ConfigParser):
    def as_dict(self):
        _dict = dict(self._sections)
        for k in _dict:
            _dict[k] = dict(self._defaults, **_dict[k])
            _dict[k].pop("__name__", None)
        return _dict


def parse_config_ini(path, section=None):
    """parse an ini config file"""
    conf = MyParser()
    conf.read(path)
    conf = conf.as_dict()
    if section is not None:
        return conf[section]
    return conf


def parse_config_json(path, section=None):
    """parse a json config file"""
    with open(path, "r", encoding="utf-8") as fid:
        data = json.load(fid)
    if section is not None:
        return data[section]
    return data


def parse_config(path, section=None):
    """
    Parse a config in any format

    Note: this rtelies on a try-catch-all; as a consequence, this method
    will not provide much details on the exception that cause the failure

    :param path: the path to the config file to be read in
    :param section: what section to extract from the config
    """

    parsers = [
        parse_config_ini,
        parse_config_json,
    ]

    for parser in parsers:
        try:
            return parser(path, section=section)
        except:  # pylint: disable=bare-except
            pass
    raise RuntimeError("loading config failed")


def add_order_data_to_config(path, data):
    config = parse_config(path)
    config["orders"].update(data)
    with open(path, "w", encoding="utf-8") as outfile:
        json.dump(config, outfile, indent=4, sort_keys=True)
