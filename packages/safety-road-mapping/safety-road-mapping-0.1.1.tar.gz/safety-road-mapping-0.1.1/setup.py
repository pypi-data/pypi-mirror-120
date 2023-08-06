# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safety_road_mapping', 'safety_road_mapping.docs']

package_data = \
{'': ['*'],
 'safety_road_mapping': ['maps/*', 'notebooks/*', 'notebooks/data/.gitignore'],
 'safety_road_mapping.docs': ['source/*']}

install_requires = \
['Unidecode>=1.2.0,<2.0.0',
 'colour>=0.1.5,<0.2.0',
 'folium>=0.12.1,<0.13.0',
 'geopy>=2.2.0,<3.0.0',
 'openrouteservice>=2.3.3,<3.0.0',
 'pandas>=1.3.2,<2.0.0',
 'patool>=1.12,<2.0',
 'plotly>=5.2.2,<6.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'typeguard>=2.12.1,<3.0.0']

setup_kwargs = {
    'name': 'safety-road-mapping',
    'version': '0.1.1',
    'description': 'Module to generate a safety score for brazilian roads.',
    'long_description': "# General Instructions\n\n## Generating API token\n\nThis project uses [openrouteservice API](https://openrouteservice.org) to plot maps and routes.\nSo the following steps are necessary at first:\n\n1. Sign up on [openrouteservice.org](https://openrouteservice.org/dev/#/signup) to generate an API token;\n2. Rename the `.env.example` file inside `safety_road_mapping/` folder to `.env`;\n3. Insert the generated token in the front of `TOKEN=`.\n\n## Accident road data\n\nThe accidents data used were extracted from the Polícia Rodoviária Federal website.\nThe notebook `get_data.ipynb` inside `safety_road_mapping/notebooks` folder is responsible to download and extract the data used. If you want to directly download the files you can [click here](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-acidentes).\n\n## Roadmap\n\n- The accidents data used comes just from federal police source, so there are some routes that don't receive score because they are state highways.\n- The routes subsections are not connected, once they are plotted individually in the map. Visually it can be interesting to connect them. (Is it possible or necessary?)\n",
    'author': 'Gabriel Aparecido Fonseca',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cervejaria-ambev/safety_road_mapping',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
