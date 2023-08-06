import setuptools

setuptools.setup(
    name="mxsearchstorage",
    version="1.0.0",
    author="blake",
    author_email="huiblake.li@walmart.com",
    description="Mexico search object store Library",
    packages=['mxsearchstorage'],
    install_requires = ['azure-core','azure-storage-blob','certifi','charset-normalizer',
                        'cryptography','idna','isodate', 'msrest', 'oauthlib', 'pycparser',
                        'requests', 'requests-oauthlib', 'six', 'urllib3']
)

