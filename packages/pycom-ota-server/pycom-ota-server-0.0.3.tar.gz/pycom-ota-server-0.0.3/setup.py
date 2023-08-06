import setuptools
from distutils.core import setup

with open('README.md', 'r') as f:
    long_description = f.read()

pkg_info = {}
with open('src/ota_server/_version.py', 'r') as f:
    exec(f.read(), pkg_info)

setup(
    name="pycom-ota-server",
    version=pkg_info['__version__'],
    description="Pycom OTA firmware server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="snebot",
    author_email="snebot@bitgrup.com",
    url="https://github.com/snebot-bg/pycom-ota-server",
    keywords=[],
    classifiers=[],
    package_dir={ "": "src" },
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'click==8.0.1',
        'Flask==2.0.1',
        'Flask-Classful==0.14.2',
        'itsdangerous==2.0.1',
        'Jinja2==3.0.1',
        'MarkupSafe==2.0.1',
        'packaging==21.0',
        'pyparsing==2.4.7',
        'Werkzeug==2.0.1'
    ]
)
