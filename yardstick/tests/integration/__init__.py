import unittest, pkgutil

def suite():
    return unittest.TestLoader().discover("yardstick.tests.integration", pattern="test_*.py")

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            exec ('%s = obj' % obj.__name__)
