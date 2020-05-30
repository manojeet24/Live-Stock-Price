"""
Copyright 2013 Dustin Frisch<fooker@lab.sh>

This file is part of require.

require is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

require is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with require.  If not, see <http://www.gnu.org/licenses/>.
"""

import functools


__all__ = ['require',
           'export',
           'extend',
           'oneshot',
           'singleton']



class Export(object):
    """ Wrapper for an exported factory.

        The wrapper manages the instance creation using the wrapped factory by
        calling the factory on the first requirement. The created instance is
        stored in a singleton manner and returned on further requirements.

        The export also manages the registered extends for the factory. These
        extends are called after instance creation to manipulate the instance.
    """

    def __init__(self,
                 factory,
                 scope):
        self.__factory = factory
        self.__extenders = []

        # Build a factory proxy by binding the factory function to the scope
        # function wrapper (this uses late binding allowing the create function
        # to be mocked for testing)
        self.__proxy = scope(lambda: self.create())


    def extend(self, extender):
        """ Extends this export.

            The instance created by the wrapped factory is extended by passing the
            created instance to the given extender function after creation.

            The extend function must accept the instance as its only argument. If
            the function returns a value which is not None, the instance is replaced
            with the returned value.
        """

        self.__extenders.append(extender)

        return extender


    def __call__(self):
        """ Returns an instance of this export.
        """

        return self.__proxy()


    def create(self):
        """ Creates a new instance.

            The instance is created by calling the exported factory and
            applying all extenders in the order of registration.
        """

        # Lazily create the instance by calling the factory
        instance = self.__factory()

        # Call all extenders for this export to update or replace the instance
        for extender in self.__extenders:
            # If the extender is an export, instantiate it
            if isinstance(extender, Export):
                extender = extender()

            extended = extender(instance)

            # If the extender returned a not-none value, the instance is
            # replaced with the returned value
            if extended is not None:
                instance = extended

        return instance


    @staticmethod
    def load(requirement):
        """ Loads an export by the given name.

            The name must be a full specified identifier where the module name and
            the factory name are separated by a colon. The module containing the
            export is imported using the current context and the export is retrieved
            from the module.
        """

        module, export = requirement.split(':', 1)

        # Import the module containing the export
        module = __import__(name = module,
                            globals = globals(),
                            locals = locals(),
                            fromlist = [export],
                            level = 0)

        # Get the export from the imported module
        export = getattr(module, export)

        # Check if the given name refers a exported factory
        if not isinstance(export, Export):
            raise TypeError('%s is not exported' % requirement)

        return export



def oneshot(export):
    """ Scope 'oneshot'.

        The scope does not apply any caching or reusing of exported objects.
        Each request for en export wil recreate the exported object.
    """
    return export



def singleton(export):
    """ Scope 'singleton'.

        The singleton scope ensures, that only one single instance exists
        during application life-time. The instance is created on first request
        and cached for later use.
    """
    def wrapper():
        if wrapper.instance is None:
            wrapper.instance = export()

        return wrapper.instance
    wrapper.instance = None

    return wrapper



def require(requirement=None,
            **requirements):
    """ Factory for a function decorator or property descriptor.
        Decorator to inject requirements into a function.

        The property is created by passing a single unnamed requirement to the
        function and returns the required instance.

        The decorated function is returned if the first parameter is not set
        and the keyword arguments are passed. The decorated function is wrapped
        in a way that calls the wrapped function with a named argument for each
        specified requirement containing the exported instances.
    """

    if requirement:
        # Load the export specified in the requirement
        export = Export.load(requirement)

        # Build a property accessor returning the required instance
        return property(lambda inst: export())

    elif requirements:
        # Load all exports as specified in the requirements
        exports = {name: Export.load(requirements[name])
                   for name
                   in requirements}

        def wrapper(func):
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                # Populate the keyword arguments dicts passed to the wrapped
                # function with the required instances
                kwargs.update({name: exports[name]()
                               for name
                               in exports
                               if name not in kwargs})

                # Call the wrapped function
                return func(*args,
                            **kwargs)

            return wrapped
        return wrapper

    else:
        # Assume a empty decorator function
        return lambda func: func



def export(scope=singleton,
           **requirements):
    """ Decorator to export a factory.

        Requirements for the factory can be specified. These requirements are
        passed to the wrapped function as specified by the `require` decorator.
    """

    def wrapper(func):
        return Export(factory=require(**requirements)(func),
                      scope=scope)

    return wrapper



def extend(requirement,
           **requirements):
    """ Decorator to extend a export.

        The decorated function is used to extend the export specified by the given
        name.

        Requirements for the factory can be specified. These requirements are
        passed to the wrapped function as specified by the `require` decorator.
    """

    def wrapper(func):
        return Export.load(requirement).extend(extender=require(**requirements)(func))

    return wrapper
