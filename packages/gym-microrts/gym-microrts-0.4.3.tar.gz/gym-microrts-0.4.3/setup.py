# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gym_microrts', 'gym_microrts.envs']

package_data = \
{'': ['*'],
 'gym_microrts': ['microrts/*',
                  'microrts/data/ahtn/*',
                  'microrts/data/bayesianmodels/pretrained/*',
                  'microrts/lib/*',
                  'microrts/maps/*',
                  'microrts/maps/10x10/*',
                  'microrts/maps/12x12/*',
                  'microrts/maps/16x16/*',
                  'microrts/maps/24x24/*',
                  'microrts/maps/4x4/*',
                  'microrts/maps/6x6/*',
                  'microrts/maps/8x8/*',
                  'microrts/maps/BroodWar/*',
                  'microrts/resources/*',
                  'microrts/src/*',
                  'microrts/src/ai/*',
                  'microrts/src/ai/abstraction/*',
                  'microrts/src/ai/abstraction/cRush/*',
                  'microrts/src/ai/abstraction/partialobservability/*',
                  'microrts/src/ai/abstraction/pathfinding/*',
                  'microrts/src/ai/ahtn/*',
                  'microrts/src/ai/ahtn/domain/*',
                  'microrts/src/ai/ahtn/domain/LispParser/*',
                  'microrts/src/ai/ahtn/planner/*',
                  'microrts/src/ai/ahtn/visualization/*',
                  'microrts/src/ai/core/*',
                  'microrts/src/ai/evaluation/*',
                  'microrts/src/ai/jni/*',
                  'microrts/src/ai/machinelearning/bayes/*',
                  'microrts/src/ai/machinelearning/bayes/featuregeneration/*',
                  'microrts/src/ai/mcts/*',
                  'microrts/src/ai/mcts/believestatemcts/*',
                  'microrts/src/ai/mcts/informedmcts/*',
                  'microrts/src/ai/mcts/mlps/*',
                  'microrts/src/ai/mcts/naivemcts/*',
                  'microrts/src/ai/mcts/uct/*',
                  'microrts/src/ai/minimax/*',
                  'microrts/src/ai/minimax/ABCD/*',
                  'microrts/src/ai/minimax/RTMiniMax/*',
                  'microrts/src/ai/montecarlo/*',
                  'microrts/src/ai/montecarlo/lsi/*',
                  'microrts/src/ai/portfolio/*',
                  'microrts/src/ai/portfolio/portfoliogreedysearch/*',
                  'microrts/src/ai/puppet/*',
                  'microrts/src/ai/rewardfunction/*',
                  'microrts/src/ai/scv/*',
                  'microrts/src/ai/scv/models/*',
                  'microrts/src/ai/socket/*',
                  'microrts/src/ai/stochastic/*',
                  'microrts/src/gui/*',
                  'microrts/src/gui/frontend/*',
                  'microrts/src/rts/*',
                  'microrts/src/rts/units/*',
                  'microrts/src/tests/*',
                  'microrts/src/tests/bayesianmodels/*',
                  'microrts/src/tests/sockets/*',
                  'microrts/src/tournaments/*',
                  'microrts/src/util/*']}

install_requires = \
['JPype1>=1.3.0,<2.0.0', 'gym>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'gym-microrts',
    'version': '0.4.3',
    'description': '',
    'long_description': None,
    'author': 'Costa Huang',
    'author_email': 'costa.huang@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
