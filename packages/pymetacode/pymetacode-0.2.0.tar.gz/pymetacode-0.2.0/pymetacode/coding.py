"""
The actual code generators of the pymetacode package.

Currently, there are four types of code generators:

* :class:`pymetacode.coding.PackageCreator`

  Generates the basic package structure.

* :class:`pymetacode.coding.ModuleCreator`

  Adds a module to an existing package.

* :class:`pymetacode.coding.ClassCreator`

  Adds a class to an existing module, including a test class.

* :class:`pymetacode.coding.FunctionCreator`

  Adds a function to an existing module, including a test class.

Each of these generators uses templates in the ``templates`` subdirectory of
the pymetacode package.

"""
import os
import shutil
import stat
import subprocess
import warnings

from pymetacode import configuration, utils


class PackageCreator:
    """
    Generate the basic package structure.

    The basic package structure follows Python best practices and has been
    used in a number of packages by the author of this package. In short,
    the modules reside in a subdirectory with the same name as the package,
    and parallel to that are directories for tests and documentation (
    "tests", "docs").

    Furthermore, a "setup.py" file is created to have the package
    installable using pip, and a license ("LICENSE") and readme ("README.rst")
    file are present.

    The package version is stored in the file "VERSION", a ".gitignore" file
    exists as well in the package root, and depending on the configuration,
    a git repository is initialised within the package root directory. In
    this case, a pre-commit hook is installed as well incrementing the
    version number for each commit, using the file "incrementVersion.sh"
    from the "bin" directory.


    Attributes
    ----------
    name : :class:`str`
        Name of the package to be created.

        Will usually be read from the configuration.

    subdirectories : :class:`list`
        Directories and subdirectories created within the package root.

    configuration : :class:`pymetacode.configuration.Configuration`
        Configuration as usually read from the configuration file.

    documentation : :class:`dict`
        Settings for creating the documentation.


    Examples
    --------
    The following examples demonstrate how to use the CLI from the terminal,
    rather than how to use this class programmatically.

    The first step when creating a new package is to write a config file
    that can be filled with sensible content afterwards:

    .. code-block:: bash

        pymeta write config to mypackage_config.yaml

    This would write the default configuration to "mypackage_config.yaml".
    Change all values in this file according to your needs. Afterwards,
    you can create the basic structure of your new project:

    .. code-block:: bash

        pymeta create package from mypackage_config.yaml

    Now, you have a complete package that is installable and deployable.

    """

    def __init__(self):
        self.name = ''
        self.subdirectories = [
            'tests',
            os.path.join('docs', 'api'),
            'bin']
        self.configuration = configuration.Configuration()
        self.documentation = {
            'pages': ['audience', 'changelog', 'developers', 'installing',
                      'people', 'roadmap', 'usecases']
        }

    def create(self, name=''):
        """
        Generate the basic package structure.

        Parameters
        ----------
        name : :class:`str`
            Name of the package to create.

            If provided, this will set the :attr:`name` attribute of the class.

        """
        if name:
            self.name = name
        elif not self.name:
            raise ValueError
        self._create_subdirectories()
        self._create_init_files()
        self._create_gitignore()
        self._create_prospector_profile()
        self._create_version_file()
        self._create_license_file()
        self._create_setup_py_file()
        self._create_readme_file()
        self._create_version_updater_file()
        self._create_documentation_stub()
        self._git_init()

    def _create_subdirectories(self):
        self.subdirectories.append(self.name)
        for directory in self.subdirectories:
            self._create_directory(name=os.path.join(self.name, directory))

    @staticmethod
    def _create_directory(name=''):
        if os.path.exists(name):
            warnings.warn("Directory '" + name + "' exists already.")
        else:
            os.makedirs(name)

    def _create_init_files(self):
        for directory in [self.name, 'tests']:
            init_filename = os.path.join(self.name, directory, '__init__.py')
            utils.ensure_file_exists(init_filename)

    def _create_gitignore(self):
        contents = utils.get_data_from_pkg_resources('gitignore')
        with open(os.path.join(self.name, '.gitignore'), 'w+', encoding='utf8')\
                as file:
            file.write(contents.decode("utf-8"))

    def _create_prospector_profile(self):
        contents = utils.get_data_from_pkg_resources('prospector.yaml')
        with open(os.path.join(self.name, '.prospector.yaml'), 'w+',
                  encoding='utf8') as file:
            file.write(contents.decode("utf-8"))

    def _create_version_file(self):
        with open(os.path.join(self.name, 'VERSION'), 'w+', encoding='utf8') \
                as file:
            file.write('0.1.0.dev0\n')

    def _create_license_file(self):
        template = utils.Template(
            package_path='templates/licenses',
            template='bsd-2clause.j2.txt',
            context=self.configuration.to_dict(),
            destination=os.path.join(self.name, 'LICENSE'),
        )
        template.create()

    def _create_setup_py_file(self):
        template = utils.Template(
            package_path='templates',
            template='setup.j2.py',
            context=self.configuration.to_dict(),
            destination=os.path.join(self.name, 'setup.py'),
        )
        template.create()

    def _create_readme_file(self):
        template = utils.Template(
            package_path='templates',
            template='README.j2.rst',
            context=self.configuration.to_dict(),
            destination=os.path.join(self.name, 'README.rst'),
        )
        template.create()

    def _create_version_updater_file(self):
        contents = utils.get_data_from_pkg_resources('incrementVersion.sh')
        destination = os.path.join(self.name, 'bin', 'incrementVersion.sh')
        with open(destination, 'w+', encoding='utf8') as file:
            file.write(contents.decode("utf-8"))
        os.chmod(destination, os.stat(destination).st_mode | stat.S_IXUSR)

    def _create_documentation_stub(self):
        self._create_documentation_generator_files()
        self._create_documentation_config()
        self._create_documentation_index()
        self._create_documentation_api_index()
        self._create_documentation_contents()
        self._create_documentation_multiversion_templates()

    def _create_documentation_generator_files(self):
        make_files = ['make.bat', 'Makefile']
        for file in make_files:
            contents = \
                utils.get_data_from_pkg_resources('/'.join(['docs', file]))
            destination = os.path.join(self.name, 'docs', file)
            with open(destination, 'w+', encoding='utf8') as doc_file:
                doc_file.write(contents.decode("utf-8"))

    def _create_documentation_index(self):
        shutil.copyfile(
            os.path.join(self.name, 'README.rst'),
            os.path.join(self.name, 'docs', 'index.rst')
        )
        template = utils.Template(
            package_path='templates/docs',
            template='main-toctree.j2.rst',
            context=self.configuration.to_dict(),
            destination=os.path.join(self.name, 'docs', 'index.rst'),
        )
        template.append()

    def _create_documentation_config(self):
        template = utils.Template(
            package_path='templates/docs',
            template='conf.j2.py',
            context=self.configuration.to_dict(),
            destination=os.path.join(self.name, 'docs', 'conf.py'),
        )
        template.create()

    def _create_documentation_api_index(self):
        template = utils.Template(
            package_path='templates/docs',
            template='api_index.j2.rst',
            context=self.configuration.to_dict(),
            destination=os.path.join(self.name, 'docs', 'api', 'index.rst'),
        )
        template.create()

    def _create_documentation_contents(self):
        for name in self.documentation['pages']:
            template = utils.Template(
                package_path='templates/docs',
                template='{}.j2.rst'.format(name),
                context=self.configuration.to_dict(),
                destination=os.path.join(self.name, 'docs',
                                         '{}.rst'.format(name)),
            )
            template.create()

    def _create_documentation_multiversion_templates(self):
        os.mkdir(os.path.join(self.name, 'docs', '_templates'))
        make_files = ['page.html', 'versions.html']
        for file in make_files:
            contents = \
                utils.get_data_from_pkg_resources(
                    '/'.join(['docs', '_templates', file]))
            destination = os.path.join(self.name, 'docs', '_templates', file)
            with open(destination, 'w+', encoding='utf8') as doc_file:
                doc_file.write(contents.decode("utf-8"))

    def _git_init(self):
        if self.configuration.package['git']:
            subprocess.run(["git", "init"], cwd=self.name, check=False)
            with utils.change_working_dir(os.path.join(self.name, '.git',
                                                       'hooks')):
                with open('pre-commit', 'w+', encoding='utf8') as file:
                    file.write('#!/bin/sh\n')
                    file.write('./bin/incrementVersion.sh\n')
                shutil.copymode('pre-commit.sample', 'pre-commit')


class ModuleCreator:
    """
    Add a module to an existing package.

    Actually, adding a module consists of creating three files: the module
    itself, an accompanying test module, and the API documentation file. The
    latter gets added to the API toctree directive as well.


    Attributes
    ----------
    name : :class:`str`
        Name of the module to be created.

    configuration : :class:`pymetacode.configuration.Configuration`
        Configuration as usually read from the configuration file.

    Raises
    ------
    ValueError
        Raised if no name is provided


    Examples
    --------
    The following examples demonstrate how to use the CLI from the terminal,
    rather than how to use this class programmatically.

    Prerequisite for using the CLI is to have the package configuration
    stored within the package root directory in the file
    ".project_configuration.yaml". This will be the case if the package has
    been created by the CLI as well. Furthermore, all following commands
    need to be issued from *within* the root directory of your package.

    .. code-block:: bash

        pymeta add module mymodule

    This will add a module "mymodule" to your package, together with a
    "test_mymodule" module in the "tests" subdirectory. And even better,
    the API documentation will be updated as well for you.

    """

    def __init__(self):
        self.name = ''
        self.configuration = configuration.Configuration()

    def create(self, name=''):
        """
        Add a module to an existing package.

        Parameters
        ----------
        name : :class:`str`
            Name of the module to add.

            If provided, this will set the :attr:`name` attribute of the class.

        """
        if name:
            self.name = name
        elif not self.name:
            raise ValueError
        self._create_module()
        self._create_test_module()
        self._create_api_documentation()
        self._add_api_documentation_to_toctree()

    def _create_module(self):
        filename = os.path.join(self.configuration.package['name'],
                                self.name + '.py')
        if os.path.exists(filename):
            warnings.warn("Module '{}' exists already".format(filename))
            return
        context = self.configuration.to_dict()
        context['module'] = {'name': self.name}
        template = utils.Template(
            package_path='templates/code',
            template='module.j2.py',
            context=context,
            destination=filename,
        )
        template.create()

    def _create_test_module(self):
        filename = os.path.join('tests', 'test_{}.py'.format(self.name))
        if os.path.exists(filename):
            warnings.warn("Module '{}' exists already".format(filename))
            return
        context = self.configuration.to_dict()
        context['module'] = {'name': self.name}
        template = utils.Template(
            package_path='templates/code',
            template='test_module.j2.py',
            context=context,
            destination=filename,
        )
        template.create()

    def _create_api_documentation(self):
        package = self.configuration.package['name']
        filename = os.path.join('docs', 'api', '{}.{}.rst'.format(package,
                                                                  self.name))
        if os.path.exists(filename):
            warnings.warn("File '{}' exists already".format(filename))
            return
        context = self.configuration.to_dict()
        context['module'] = {'name': self.name}
        context['header_extension'] = \
            (len(package) + len(self.name) + 1) * '='
        template = utils.Template(
            package_path='templates/docs',
            template='api_module.j2.rst',
            context=context,
            destination=filename,
        )
        template.create()

    def _add_api_documentation_to_toctree(self):
        index_filename = os.path.join('docs', 'api', 'index.rst')
        if not os.path.exists(index_filename):
            return
        with open(index_filename, encoding='utf8') as file:
            contents = file.read()
        lines = contents.split('\n')
        package = self.configuration.package['name']
        start_of_toctree = lines.index('.. toctree::')
        end_of_toctree = lines[start_of_toctree:].index('')
        lines.insert(start_of_toctree + end_of_toctree - 1,
                     '    {}.{}'.format(package, self.name))
        # Sort entries
        new_end_of_toctree = lines[start_of_toctree:].index('')
        start_sort = start_of_toctree + end_of_toctree - 1
        end_sort = start_of_toctree + new_end_of_toctree
        lines[start_sort:end_sort] = sorted(lines[start_sort:end_sort])
        with open(index_filename, "w+", encoding='utf8') as file:
            file.write('\n'.join(lines))


class ClassCreator:
    """
    Add a class to an existing module, including a test class.

    When a class is added to a module, it will always be added to the bottom
    of the module file, and at the same time a test class with a very basic
    setup and a first test will be added to the corresponding test module.


    Attributes
    ----------
    name : :class:`str`
        Name of the class to be added to the module

    module : :class:`str`
        Name of the module the class should be added to

    configuration : :class:`pymetacode.configuration.Configuration`
        Configuration as usually read from the configuration file.

    Raises
    ------
    ValueError
        Raised if no class or module name is provided


    Examples
    --------
    The following examples demonstrate how to use the CLI from the terminal,
    rather than how to use this class programmatically.

    Prerequisite for using the CLI is to have the package configuration
    stored within the package root directory in the file
    ".project_configuration.yaml". This will be the case if the package has
    been created by the CLI as well. Furthermore, all following commands
    need to be issued from *within* the root directory of your package.

    .. code-block:: bash

        pymeta add class MyClass to mymodule

    This will add the class "MyClass" to the module "mymodule", together with a
    test class in the "test_mymodule" module. The class will come with a
    basic docstring, and the test class with a minimalistic setup and first
    test (for implementation of the class) that gets you started with
    writing further tests.

    """

    def __init__(self):
        self.name = ''
        self.module = ''
        self.configuration = configuration.Configuration()
        self._module_filename = ''
        self._package_version = ''

    def create(self, name='', module=''):
        """
        Create actual code stub for the class.

        Parameters
        ----------
        name : :class:`str`
            Name of the function to be created

        module : :class:`str`
            Name of the module the function should be added to

        Raises
        ------
        ValueError
            Raised if function or module name is missing

        """
        self._check_prerequisites(module, name)
        self._create_class()
        self._create_test_class()

    def _check_prerequisites(self, module, name):
        if name:
            self.name = name
        elif not self.name:
            raise ValueError('Class name missing')
        if module:
            self.module = module
        elif not self.module:
            raise ValueError('Module name missing')
        package = self.configuration.package['name']
        self._module_filename = os.path.join(package,
                                             '{}.py'.format(self.module))
        if not os.path.exists(self._module_filename):
            raise ValueError('Module {} does not exist'.format(self.module))
        if not self._package_version:
            version = utils.package_version_from_file()
            self._package_version = '.'.join(version.split('.')[0:2])

    def _create_class(self):
        context = self.configuration.to_dict()
        context['class'] = {'name': self.name}
        context['package'] = {'version': self._package_version}
        template = utils.Template(
            package_path='templates/code',
            template='class.j2.py',
            context=context,
            destination=self._module_filename,
        )
        template.append()

    def _create_test_class(self):
        context = self.configuration.to_dict()
        context['class'] = {
            'name': self.name,
            'instance': utils.camel_case_to_underscore(self.name),
        }
        context['module'] = {'name': self.module}
        filename = os.path.join('tests', 'test_{}.py'.format(self.module))
        template = utils.Template(
            package_path='templates/code',
            template='test_class.j2.py',
            context=context,
            destination=filename,
        )
        template.append()


class FunctionCreator:
    """
    Add a function to an existing module, including a test class.

    When a function is added to a module, it will always be added to the bottom
    of the module file, and at the same time a test class with a first test
    will be added to the corresponding test module.


    Attributes
    ----------
    name : :class:`str`
        Name of the function to be added to the module

    module : :class:`str`
        Name of the module the function should be added to

    configuration : :class:`pymetacode.configuration.Configuration`
        Configuration as usually read from the configuration file.

    Raises
    ------
    ValueError
        Raised if no function or module name is provided


    Examples
    --------
    The following examples demonstrate how to use the CLI from the terminal,
    rather than how to use this class programmatically.

    Prerequisite for using the CLI is to have the package configuration
    stored within the package root directory in the file
    ".project_configuration.yaml". This will be the case if the package has
    been created by the CLI as well. Furthermore, all following commands
    need to be issued from *within* the root directory of your package.

    .. code-block:: bash

        pymeta add function my_function to mymodule

    This will add the function "my_function" to the module "mymodule", together
    with a test class in the "test_mymodule" module. The function will come
    with a basic docstring, and the test class with a minimalistic first
    test that gets you started with writing further tests.

    """

    def __init__(self):
        self.name = ''
        self.module = ''
        self.configuration = configuration.Configuration()
        self._module_filename = ''
        self._package_version = ''

    def create(self, name='', module=''):
        """
        Create actual code stub for the function.

        Parameters
        ----------
        name : :class:`str`
            Name of the function to be created

        module : :class:`str`
            Name of the module the function should be added to

        Raises
        ------
        ValueError
            Raised if function or module name is missing

        """
        self._check_prerequisites(module, name)
        self._create_function()
        self._create_test_class()

    def _check_prerequisites(self, module, name):
        if name:
            self.name = name
        elif not self.name:
            raise ValueError('Function name missing')
        if module:
            self.module = module
        elif not self.module:
            raise ValueError('Module name missing')
        package = self.configuration.package['name']
        self._module_filename = os.path.join(package,
                                             '{}.py'.format(self.module))
        if not os.path.exists(self._module_filename):
            raise ValueError('Module {} does not exist'.format(self.module))
        if not self._package_version:
            version = utils.package_version_from_file()
            self._package_version = '.'.join(version.split('.')[0:2])

    def _create_function(self):
        context = self.configuration.to_dict()
        context['function'] = {'name': self.name}
        context['package'] = {'version': self._package_version}
        template = utils.Template(
            package_path='templates/code',
            template='function.j2.py',
            context=context,
            destination=self._module_filename,
        )
        template.append()

    def _create_test_class(self):
        context = self.configuration.to_dict()
        context['function'] = {
            'name': self.name,
            'name_camelcase': utils.underscore_to_camel_case(self.name),
        }
        context['module'] = {'name': self.module}
        filename = os.path.join('tests', 'test_{}.py'.format(self.module))
        template = utils.Template(
            package_path='templates/code',
            template='test_function.j2.py',
            context=context,
            destination=filename,
        )
        template.append()
