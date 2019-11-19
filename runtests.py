#!/usr/bin/env python3

import unittest

def runtests():
    suite = unittest.TestLoader().discover('tests', pattern='test*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    runtests()
