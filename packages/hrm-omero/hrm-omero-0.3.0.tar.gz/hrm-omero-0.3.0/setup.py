# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hrm_omero']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'loguru>=0.5.3,<0.6.0',
 'omero-py>=5.9.0,<6.0.0']

entry_points = \
{'console_scripts': ['ome-hrm = hrm_omero.cli:main']}

setup_kwargs = {
    'name': 'hrm-omero',
    'version': '0.3.0',
    'description': 'A connector between the Huygens Remote Manager (HRM) and OMERO.',
    'long_description': '# The HRM-OMERO connector\n\nThis project provides a connector to allow for communication between an [HRM (Huygens\nRemote Manager)][1] and an [OMERO server][2].\n\nIts purpose is to simplify the data transfer by allowing raw images to be downloaded\nfrom OMERO as well as uploading deconvolution results back to OMERO directly from within\nthe HRM web interface.\n\n## Installation\n\n### Distributions that include Python 3.6 or newer (e.g. Ubuntu 20.04)\n\n```bash\npip install hrm-omero\n```\n\n### CentOS 6\n\n[CentOS 6][co6] is EOL since 2020-11-30, so you should really consider upgrading to a newer\nrelease. However, we know that sometimes this is not easily doable due to dependencies,\nhardware support or whatever reason - so here are instructions to make the connector\nwork on that old distribution.\n\nIt\'s strongly recommended to use [pyenv][3] for installing *Python 3.6*, which is the\nabsolute minimum for using the HRM-OMERO connector (or its actual dependencies, to be\nfully correct). In case you don\'t want *pyenv* to mess with your system setup, you can\nsimply ask it to install that version somewhere and then only create a *virtual\nenvironment* from it using the `--copies` flag - this will result in a standalone\nsetup that won\'t affect anything else on the system.\n\n```bash\n# install the build-time requirements for Python 3.6 and Java 1.8 for Bio-Formats\nsudo yum install openssl-devel readline-devel gcc-c++ java-1.8.0-openjdk\n\n# get pyenv and put it into your home directory or wherever you prefer it to be\ngit clone https://github.com/pyenv/pyenv.git ~/.pyenv\n\n# activate pyenv *FOR THIS SHELL ONLY* (needs to be done whenever you want to use it)\nexport PYENV_ROOT="$HOME/.pyenv"\nexport PATH="$PYENV_ROOT/bin:$PATH"\neval "$(pyenv init --path)"\neval "$(pyenv init -)"\n\n# ask pyenv to install Python 3.6.15 (will end up in "~/.pyenv/versions/3.6.15/")\npyenv install 3.6.15  # takes a bit (compiling...)\n\n# create a bare, stand-alone Python 3.6 virtual environment\n~/.pyenv/versions/3.6.15/bin/python -m venv --copies /opt/venvs/hrm-omero\n\n# now you can install the connector into this virtual environment - please note that the\n# installation takes quite a while (~15min) as it needs to build the ZeroC Ice bindings\n/opt/venvs/hrm-omero/bin/pip install hrm-omero\n\n# from now on you can simply call the connector using its full path, there is no need\n# to pre-activate the virtual environment - you could even drop your pyenv completely:\n/opt/venvs/hrm-omero/bin/ome-hrm --help\n\n# this is even usable as a drop-in replacement for the legacy `ome_hrm.py` script:\ncd $PATH_TO_YOUR_HRM_INSTALLATION/bin\nmv "ome_hrm.py" "__old__ome_hrm.py"\nln -s "/opt/venvs/hrm-omero/bin/ome-hrm" "ome_hrm.py"\n```\n\n## Debugging\n\nBy default the connector will be rather silent as otherwise the log files will be\ncluttered up quite a bit on a production system. However, it is possible to increase the\nlog level by specifying `-v`, `-vv` and so on.\n\nCurrently it is not yet possible to ajust the log level that is being used when operated\nthrough the HRM web interface (which is the default). To do so, have a look in the\n`hrm_omero.cli.run_task()` function. Log messages produced by the connector when called\nby HRM will usually end up in the web server\'s error log (as they go to `stderr`).\n\n## Example Usage\n\nStore you username and password in variables:\n\n```bash\nread OMEROUSER\nread OMEROPW\n```\n\n### Verifying Credentials\n\n```bash\nome-hrm \\\n    --user $OMEROUSER \\\n    --password $OMEROPW \\\n    checkCredentials\n```\n\n### Fetching OMERO tree information\n\nSet the `--id` parameter according to what part of the tree should be retrieved:\n\n```bash\nOMERO_ID="ROOT"                # fetches the base tree view for the current user\nOMERO_ID="G:4:Experimenter:9"  # fetches the projects of user \'9\' in group \'4\'\nOMERO_ID="G:4:Project:12345"   # fetches the datasets of project \'12345\'\nOMERO_ID="G:4:Dataset:65432"   # lists the images of dataset \'65432\'\n```\n\nThen run the actual command to fetch the information, the result will be a JSON tree:\n\n```bash\nome-hrm \\\n    --user $OMEROUSER \\\n    --password $OMEROPW \\\n    retrieveChildren \\\n    --id "$OMERO_ID"\n```\n\nFor example this could be the output when requesting `"G:4:Dataset:65432"`:\n\n```json\n[\n    {\n        "children": [],\n        "class": "Image",\n        "id": "G:4:Image:1311448",\n        "label": "4321_mko_ctx_77.tif",\n        "owner": "somebody"\n    },\n    {\n        "children": [],\n        "class": "Image",\n        "id": "G:4:Image:1566150",\n        "label": "test-image.tif",\n        "owner": "somebody"\n    }\n]\n```\n\n### Downloading an image from OMERO\n\nThis will fetch the second image from the example tree above and store it in `/tmp/`:\n\n```bash\nome-hrm \\\n    --user $OMEROUSER \\\n    --password $OMEROPW \\\n    OMEROtoHRM \\\n    --imageid "G:4:Image:1566150" \\\n    --dest /tmp/\n```\n\n### Uploading an image from the local file system to OMERO\n\nThe command below will import a local image file into the example dataset from above:\n\n```bash\nome-hrm \\\n    --user $OMEROUSER \\\n    --password $OMEROPW \\\n    HRMtoOMERO \\\n    --dset "G:4:Dataset:65432" \\\n    --file test-image.tif\n```\n\n[1]: https://huygens-rm.org/\n[2]: https://www.openmicroscopy.org/omero/\n[3]: https://github.com/pyenv/pyenv\n[co6]: https://wiki.centos.org/About/Product\n',
    'author': 'Niko Ehrenfeuchter',
    'author_email': 'nikolaus.ehrenfeuchter@unibas.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imcf/hrm-omero',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
