import os
import sys
from paver.easy import *
from paver.setuputils import setup
import paver.doctools

PROJECT_PATH = path(__file__).abspath().dirname()

@task
def clean():
    '''
    Delete all compiled files in the source directory
    '''
    for pyc in PROJECT_PATH.walkfiles('*.pyc'):
        os.remove(pyc)
