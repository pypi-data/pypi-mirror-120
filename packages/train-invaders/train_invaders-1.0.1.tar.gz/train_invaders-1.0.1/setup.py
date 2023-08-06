# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['train_invaders']

package_data = \
{'': ['*'], 'train_invaders': ['assets/*']}

install_requires = \
['ipython>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'train-invaders',
    'version': '1.0.1',
    'description': 'Jupyter Notebook + Space Invaders!?',
    'long_description': '<h1 align="center">\n  <br>\n  <img src="https://raw.githubusercontent.com/aporia-ai/TrainInvaders/main/src/assets/logo.png" alt="TrainInvaders" width="200">\n  <br>\n    Train Invaders\n    <a href="https://twitter.com/intent/tweet?text=Jupyter%20Notebook%20%2B%20Space%20Invaders%3F!%20Something%20fun%20to%20do%20while%20training%20your%20model%20%F0%9F%91%BE&url=https://github.com/aporia-ai/TrainInvaders&hashtags=MachineLearning,JupyterNotebook,DataScience,TrainInvaders" target="_blank">\n        <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" width="70">\n    </a>\n</h1>\n\n<h4 align="center">Jupyter Notebook + Space Invaders!?</h4>\n\n<p align="center">\n  <a href="https://pypi.python.org/pypi/train_invaders/">\n    <img src="https://img.shields.io/pypi/dm/ansicolortags.svg"\n         alt="PyPI download monthly">\n  </a>\n  <img src="https://img.shields.io/badge/python-+3.6-blue.svg"\n         alt="Python version">\n  <img src="https://img.shields.io/badge/contributions-welcome-orange.svg"\n         alt="Python version">\n  <img src="https://img.shields.io/badge/license-MIT-green.svg"\n         alt="License">\n</p>\n\n<p align="center">\n  <a href="#why">Why?</a> •\n  <a href="#getting-started-">Getting started</a> •\n  <a href="#how-it-works-%EF%B8%8F">How it works</a> •\n  <a href="#faq-">FAQ</a> •\n  <a href="#drawbacks-">Drawbacks</a> •\n  <a href="#contribute-">Contribute</a> •\n  <a href="#thanks-to-">Thanks to</a> •\n  <a href="#you-may-also-like-%EF%B8%8F">You may also like...</a>\n</p>\n\n![Demo](https://raw.githubusercontent.com/aporia-ai/TrainInvaders/main/src/assets/demo.gif)\n\n## Why❓\n*Training a model can be a long long process!*\n\nIn the meantime, have a bit of fun with a **competitive space invaders game**.\n\nSee if you can get your name to the top of the *leaderboard*.\n\n## Getting started 🏁\n1. Install the game:\n`!pip3 install train_invaders --upgrade`\n2. Import the game in your notebook:\n`import train_invaders.start`\n3. Start training your model. The game will automatically pop up when the process begins.\n4. **Play the game!** *You\'ll get notified when your training is finished*.\n5. Want to stop the game from popping up when the model is being trained?\n`import train_invaders.stop` will do the work.\n\n## How it works ⚙️\n**Tons of magic**... Just kidding :)\n\nWhen importing the `start` module, its code will be executed.\n\nThe code utilizes python\'s `settrace` function which follows the functions\' call stack.\n\nWhen a function named `fit` `train` or `train_on_batch` is called - using Jupyter notebook\'s kernel, aka, `IPython`, a javascript view code will be injected inside the output block as an `iframe` to keep it completely **isolated from your code**.\n\nWhen importing the `stop` module, the `settrace` function will be canceled and the function hooks will be removed.\n\n## FAQ 🙋\n### Will it interfere with the training process somehow?\n\nNO. The game will start and be played **in parallel to the training** and will even *let you know when the training is finished*.\n\n## Drawbacks 🥺\n* Training stop indication is only in Jupyter Notebook. Want to get notified by email or text? Try [MLNotify](https://mlnotify.aporia.com/)\n* Authentication, and therefore, saving your score can only be done from `localhost` and port `8888 - 8891 / 8080 / 8081`\n\n## Contribute 🤝\nHave an awesome idea for a new feature? PRs are more than welcome!\n\n1. Clone the project\n2. Implement your idea\n3. Made changes in the game? re-compile it with `make build-game`\n4. Run `pip install . --upgrade`\n5. Test the changes in your notebook\n6. PR us!\n\n## Thanks to 🙏\n[JanSiebert](https://github.com/JanSiebert/wasm-space-invaders) for the WebAssembly game.\n\n[Cody Boisclair](https://github.com/codeman38) for the PressStart2P font.\n\n[Vue](https://github.com/vuejs/vue) for the awesome FE framework.\n\n## You may also like... ❤️\n[Aporia](https://www.aporia.com/?utm_source=train-invaders&utm_medium=docs&utm_campaign=train-invaders) - Customized monitoring for your ML models.\n\n[MLOps Toys](https://mlops.toys/?utm_source=train-invaders&utm_medium=docs&utm_campaign=train-invaders) - A curated list of useful MLOps tools.\n',
    'author': 'Aporia',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aporia-ai/TrainInvaders',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
