from distutils.core import setup
import py2exe

setup(
    windows=['main.py'],
    options={
        'py2exe': {
            'packages': ['tkinter', 'datetime', 'pytz', 'requests'],
        }
    }
)
