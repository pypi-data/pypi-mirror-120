from setuptools import setup
# https://python-packaging.readthedocs.io/en/latest/minimal.html
# python setup.py sdist upload
# python -m twine upload dist/*


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='nodewire',
      version='2.0.1',
      description='Nodewire',
      long_description=readme(),
      url='http://www.nodewire.org',
      author='Ahmad Sadiq',
      author_email='sadiq.a.ahmad@gmail.com',
      license='BSD',
      packages=['nodewire'],
      #scripts=['bin/nw_script.py', 'bin/nw_client.py' ],
      install_requires=[
            'configparser',
            'requests',
            'asyncio'
      ],
      zip_safe=False)