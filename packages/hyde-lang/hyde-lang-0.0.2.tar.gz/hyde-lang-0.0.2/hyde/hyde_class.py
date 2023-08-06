from hyde.hyde_callable import HydeCallable
from hyde.hyde_instance import HydeInstance


class HydeClass(HydeCallable):
    arity = 0

    def __init__(self, name, superclass, methods):
        self.name       = name
        self.superclass = superclass
        self.methods    = methods

    def call(self, interpreter, arguments):
        instance    = HydeInstance(self)
        initializer = self.find_method('init')

        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]

        if self.superclass is not None:
            return self.superclass.find_method(name)

    def __str__(self):
        return self.name