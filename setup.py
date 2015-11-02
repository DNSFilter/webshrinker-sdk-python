try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'webshrinker',
    packages = ['webshrinker'],
    description = 'Provides access to the Web Shrinker API services, including website category lookups.',
    author = 'Web Shrinker',
    version = '1.0',
    license = 'LICENSE.txt',
    url = 'https://github.com/webshrinker/webshrinker-sdk-python',
    download_url = 'https://github.com/webshrinker/webshrinker-sdk-python/tarball/1.0',
    install_requires = [
        "requests >= 2.8.1",
        "requests[security]"
    ]
)
