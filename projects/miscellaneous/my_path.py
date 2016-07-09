from os import path, getcwd, chdir

"""
From http://stackoverflow.com/questions/7116889/python-file-attribute-absolute-or-relative
"""

def print_my_path():
    print('cwd:      {}'.format(getcwd()))
    print('__file__: {}'.format(__file__))
    print('dir:      {}'.format(path.dirname(path.realpath(__file__))))
    print('abspath:  {}'.format(path.abspath(__file__)))

print_my_path()

print "----------"
chdir('..')

print_my_path()