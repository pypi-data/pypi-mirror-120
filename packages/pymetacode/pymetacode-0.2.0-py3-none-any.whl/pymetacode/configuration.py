"""
Configuration handling of the pymetacode package.

Key to the rather simplistic and user-friendly command-line interface (CLI)
of the pymetacode package is a configuration stored within the
package root directory and read by all the code generators residing in the
:mod:`pymetacode.coding` module.

The :class:`Configuration` class provides the necessary functionality for
creating a default configuration file as well as for reading the
configuration from a file for use with the code generators.

"""
import datetime

import oyaml as yaml

from pymetacode import utils


class Configuration(utils.ToDictMixin):
    """
    Configuration used for generating code.

    A necessary prerequisite for all the code generators is a minimal set of
    configuration values that are persistently stored in a file within the
    project root directory and read from there accordingly.

    The class provides the unique place to structure this configuration.


    Attributes
    ----------
    package : :class:`dict`
        Configuration on the package level

    documentation : :class:`dict`
        Configuration regarding the documentation of the package

    Raises
    ------
    ValueError
        Raised if no dict is provided.


    Examples
    --------
    The following examples demonstrate how to use the CLI from the terminal,
    rather than how to use this class programmatically.

    The first step when creating a new package is to write a config file
    that can be filled with sensible content afterwards:

    .. code-block:: bash

        pymeta write config to mypackage_config.yaml

    This would write the default configuration to "mypackage_config.yaml".
    Change all values in this file according to your needs.

    """

    def __init__(self):
        super().__init__()
        self.package = {
            'name': '',
            'author': '',
            'author_email': '',
            'year': datetime.date.strftime(datetime.date.today(), '%Y'),
            'description': '',
            'urls': {
                'main': '',
                'documentation': '',
                'source': '',
            },
            'keywords': [],
            'install_requires': [],
            'git': False,
        }
        self.documentation = {
            'logo': '',
            'favicon': '',
        }

    def from_dict(self, dict_=None):
        """
        Set attributes from dictionary.

        Parameters
        ----------
        dict_ : :class:`dict`
            Dictionary containing information of a task.

        Raises
        ------
        ValueError
            Raised if no dict is provided.

        """
        if not dict_:
            raise ValueError
        for key, value in dict_.items():
            if hasattr(self, key) and value:
                if isinstance(getattr(self, key), list):
                    if isinstance(value, list):
                        for element in value:
                            getattr(self, key).append(element)
                    else:
                        getattr(self, key).append(value)
                else:
                    setattr(self, key, value)

    def to_file(self, name=''):
        """
        Write to YAML file.

        Parameters
        ----------
        name : :class:`str`
            Name of the YAML file to write to.

        """
        with open(name, 'w+', encoding='utf8') as file:
            yaml.dump(self.to_dict(), file)

    def from_file(self, name=''):
        """
        Read from YAML file.

        Parameters
        ----------
        name : :class:`str`
            Name of the YAML file to read from.

        """
        with open(name, 'r', encoding='utf8') as file:
            dict_ = yaml.load(file, Loader=yaml.SafeLoader)
        self.from_dict(dict_)
