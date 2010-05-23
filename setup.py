from distutils.core import setup

try:
    long = open('README.rst').read()
except:
    long = ''

setup(
    name = "django-feedmap",
    version = '0.1',
    url = 'http://opensource.washingtontimes.com/projects/django-feedmap/',
    author = 'Justin Quick',
    description = 'Use a register command to generate RSS and Atom feeds as well as a corresponding Sitemaps. Integrates easily with ShareThis',
    long_description = long,
    packages = ['feedmap','feedmap.templatetags']
)

