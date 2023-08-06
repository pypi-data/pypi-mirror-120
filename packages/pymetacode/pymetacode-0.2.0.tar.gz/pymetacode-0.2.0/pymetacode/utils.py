"""
Auxiliary functionality used by other modules of the pymetacode package.

To avoid circular dependencies, this module does *not* depend on any other
modules of the pymetacode package, but it can be imported into every other
module.

As naturally, a utils module tends to be a bit messy, the different tools
available are listed below according to more general categories.


Files and I/O
=============

* :func:`ensure_file_exists`

  Create an (empty) file if it does not exist already.

* :func:`get_data_from_pkg_resources`

  Obtain contents from a non-code file stored within the package.

* :func:`change_working_dir`

  Context manager for temporarily changing the working directory.


String manipulation
===================

* :func:`camel_case_to_underscore`

  Change string from camel case to using underscores.

* :func:`underscore_to_camel_case`

  Change string from underscores to using camel case.


Helper classes
==============

* :class:`ToDictMixin`

  Mixin class for returning all public attributes as dict.

* :class:`Template`

  Wrapper for using the template engine (Jinja2).


Module documentation
====================
"""
import collections
import contextlib
import datetime
import os
import pkgutil
import re

import jinja2


def ensure_file_exists(name=''):
    """
    Create an (empty) file if it does not exist already.

    This is similar to the "touch" command from unixoid operating systems,
    although it does *not* change the timestamp of the file.

    Parameters
    ----------
    name : :class:`str`
        Name of the file


    Raises
    ------
    ValueError
        Raised if no filename is given.

    """
    if not name:
        raise ValueError('No filename given.')
    with open(name, 'a', encoding='utf8'):
        pass


def get_data_from_pkg_resources(name='', directory='templates'):
    """
    Obtain contents from a non-code file stored within the package.

    Rather than manually playing around with paths relative to the package
    root directory, contents non-code files need to be obtained in a way
    that works with different kinds of package installation.

    Note that in Python, only files within the package, *i.e.* within the
    directory where all the modules are located, can be accessed, not files
    that reside on the root directory of the package.

    Parameters
    ----------
    name : :class:`str`
        Name of the file whose contents should be accessed.

    directory : :class:`str`
        Directory within the package where the files are located.

        Default: "templates"

    Returns
    -------
    contents : :class:`bytes`
        Bytes array containing the contents of the non-code file.

        To convert this into a string, use the :func:`decode` function.

    """
    if not name:
        raise ValueError('No filename given.')
    contents = pkgutil.get_data(__package__, '/'.join([directory, name]))
    return contents


class ToDictMixin:
    """
    Mixin class for returning all public attributes as dict.

    Sometimes there is the need to either exclude public attributes (in case
    of infinite loops created by trying to apply ``to_dict`` in this case)
    or to add (public) attributes, particularly those used by getters and
    setters that are otherwise not included.

    To do so, there are two non_public attributes of this class each class
    inheriting from it will be able to set as well:

    * :attr:`_exclude_from_to_dict`
    * :attr:`_include_in_to_dict`

    The names should be rather telling. For details, see below.

    Attributes
    ----------
    __odict__ : :class:`collections.OrderedDict`
        Dictionary of attributes preserving the order of their definition

    _exclude_from_to_dict : :class:`list`
        Names of (public) attributes to exclude from dictionary

        Usually, the reason to exclude public attributes from being added to
        the dictionary is to avoid infinite loops, as sometimes an object
        may contain a reference to another object that in turn references back.

    _include_in_to_dict : :class:`list`
        Names of (public) attributes to include into dictionary

        Usual reasons for actively including (public) attributes into the
        dictionary are those attributes accessed by getters and setters and
        hence not automatically included in the list otherwise.

    """

    def __init__(self):
        if '__odict__' not in self.__dict__:
            self.__odict__ = collections.OrderedDict()
        self._exclude_from_to_dict = []
        self._include_in_to_dict = []

    def __setattr__(self, attribute, value):
        """
        Add attributes to :attr:`__odict__` to preserve order of definition.

        Parameters
        ----------
        attribute : :class:`str`
            Name of attribute
        value : :class:`str`
            Value of attribute

        """
        if '__odict__' not in self.__dict__:
            super().__setattr__('__odict__', collections.OrderedDict())
        self.__odict__[attribute] = value
        super().__setattr__(attribute, value)

    def to_dict(self):
        """
        Create dictionary containing public attributes of an object.

        Returns
        -------
        public_attributes : :class:`collections.OrderedDict`
            Ordered dictionary containing the public attributes of the object

            The order of attribute definition is preserved

        """
        if hasattr(self, '__odict__'):
            result = self._traverse_dict(self.__odict__)
        else:
            result = self._traverse_dict(self.__dict__)
        return result

    def _traverse_dict(self, instance_dict):
        output = collections.OrderedDict()
        for key, value in instance_dict.items():
            if str(key).startswith('_') \
                    or str(key) in self._exclude_from_to_dict:
                pass
            else:
                output[key] = self._traverse(key, value)
        for key in self._include_in_to_dict:
            output[key] = self._traverse(key, getattr(self, key))
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            result = value.to_dict()
        elif isinstance(value, (dict, collections.OrderedDict)):
            result = self._traverse_dict(value)
        elif hasattr(value, '__odict__'):
            result = self._traverse_dict(value.__odict__)
        elif hasattr(value, '__dict__'):
            result = self._traverse_dict(value.__dict__)
        elif isinstance(value, list):
            result = [self._traverse(key, i) for i in value]
        elif isinstance(value, (datetime.datetime, datetime.date,
                                datetime.time)):
            result = str(value)
        else:
            result = value
        return result


@contextlib.contextmanager
def change_working_dir(path=''):
    """
    Context manager for temporarily changing the working directory.

    Sometimes it is necessary to temporarily change the working directory,
    but one would like to ensure that the directory is reverted even in case
    an exception is raised.

    Due to its nature as a context manager, this function can be used with a
    ``with`` statement. See below for an example.


    Parameters
    ----------
    path : :class:`str`
        Path the current working directory should be changed to.


    Examples
    --------
    To temporarily change the working directory:

    .. code-block::

        with change_working_dir(os.path.join('some', 'path')):
            # Do something that may raise an exception

    This can come in quite handy in case of tests.

    """
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def camel_case_to_underscore(name=''):
    """
    Change string from camel case to using underscores.

    According to PEP8, class names should follow camel case convention,
    whereas methods, functions, and variables should use underscores.

    Parameters
    ----------
    name : :class:`str`
        Name to be changed from camel case to using underscores.

    Returns
    -------
    name : :class:`str`
        Name changed from camel case to using underscores.

    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def underscore_to_camel_case(name=''):
    """
    Change string from underscores to using camel case.

    According to PEP8, class names should follow camel case convention,
    whereas methods, functions, and variables should use underscores.

    Parameters
    ----------
    name : :class:`str`
        Name to be changed from underscores to using camel case.

    Returns
    -------
    name : :class:`str`
        Name changed from underscores to using camel case.

    """
    name = ''.join(char.capitalize() for char in name.split('_'))
    return name


class Template:
    """
    Wrapper for using the template engine (Jinja2).

    Dealing with templates requires a number of settings to be made, namely
    the source of the template, its name, the context (*i.e.*,
    the dictionary containing the variables to be replaced within the
    template), and the destination the rendered template should be output to.


    Attributes
    ----------
    package_path : :class:`str`
        Location within the package where the template resides.

    template : :class:`str`
        Name of the template to be used.

        Relative to the :attr:`package_path`.

    context : :class:`dict`
        Key-value store of variables to be replaced within the template.

    destination : :class:`str`
        Name of the file the rendered template should be output to.


    Examples
    --------
    Probably the best way to use the class is to instantiate an object
    providing all necessary parameters:

    .. code-block::

        template = Template(
            package_path='some/relative/path/to/the/template',
            template='name_of_the_template',
            context=dict(),
            destination='name_of_the_file_to_output_rendered_template_to',
        )

    Afterwards, the respective command can be issued on the template,
    depending on whether the rendered template should be written or appended
    to the destination:

    .. code-block::

        template.create()
        template.append()

    """

    def __init__(self, package_path='', template='', context=None,
                 destination=''):
        self.package_path = package_path
        self.template = template
        self.context = context
        self.destination = destination

    @property
    def environment(self):
        """
        Environment used by the template engine.

        Read-only property that gets automatically set from the class
        properties.

        Returns
        -------
        env : :class:`jinja2.Environment`
            Environment settings for the template engine.

        """
        env = jinja2.Environment(
            loader=jinja2.PackageLoader(__package__,
                                        package_path=self.package_path),
            autoescape=True,
            keep_trailing_newline=True,
        )
        return env

    def render(self):
        """
        Render the template.

        Returns
        -------
        content : :class:`str`
            Rendered template.

        """
        self._add_rst_markup_to_context()
        template = self.environment.get_template(self.template)
        return template.render(self.context)

    def create(self):
        """
        Write rendered template to a file.

        Note: If you need to *append* the rendered template to an existing
        file, you should use :meth:`append` instead.

        """
        with open(self.destination, 'w+', encoding='utf8') as file:
            file.write(self.render())

    def append(self):
        """
        Append rendered template to a file.

        Note: If you need to *output* the rendered template to a file,
        removing all previous content of this file, you should use
        :meth:`create` instead.

        """
        with open(self.destination, 'a', encoding='utf8') as file:
            file.write(self.render())

    def _add_rst_markup_to_context(self):
        if 'package' in self.context and 'name' in self.context['package']:
            length = len(self.context['package']['name'])
            rst_markup = {
                'header_hash': length * '#',
                'header_equal': length * '=',
                'header_minus': length * '-',
                'header_tilde': length * '~',
            }
            self.context['rst_markup'] = rst_markup


def package_version_from_file():
    """
    Obtain version of the given package by reading file "VERSION".

    The function attempts to read the version number from the file "VERSION"
    in the current working directory. Therefore, if this file does not
    exist, a FileNotFoundError will be raised.

    Returns
    -------
    version : :class:`str`
        Version string as contained in file "VERSION" in current directory

    """
    with open('VERSION', encoding='utf8') as file:
        version = file.read()
    return version
