# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipen_args']
install_requires = \
['diot', 'pipen', 'pyparam']

setup_kwargs = {
    'name': 'pipen-args',
    'version': '0.0.3',
    'description': 'Command-line argument parser for pipen.',
    'long_description': "# pipen-args\n\nCommand line argument parser for [pipen][1]\n\n## Usage\n```python\nfrom pipen import Proc, Pipen\nfrom pipen_args import args\n\nclass Process(Proc):\n    input = 'a'\n    input_data = range(10)\n    script = 'echo {{in.a}}'\n\nPipen().run(Process)\n```\n\n```\n> python example.py --help\n\nDESCRIPTION:\n  Pipeline description.\n\nUSAGE:\n  example.py [OPTIONS]\n\nOPTIONAL OPTIONS:\n  --profile <STR>                 - The default profile from the configuration\n                                    to run the pipeline. This profile will be\n                                    used unless a profile is specified in the\n                                    process or in the .run method of pipen.\n                                    Default: default\n  --loglevel <AUTO>               - The logging level for the main logger, only\n                                    takes effect after pipeline is initialized.\n                                    Default: <from config>\n  --cache [BOOL]                  - Whether enable caching for processes.\n                                    Default: <from config>\n  --dirsig <INT>                  - The depth to check the Last Modification\n                                    Time of a directory.\n                                    Since modifying the content won't change its\n                                    LMT.\n                                    Default: <from config>\n  --error_strategy <CHOICE>       - How we should deal with job errors.\n                                     - ignore: Let other jobs keep running.\n                                    But the process is still failing when done.\n                                     - halt: Halt the pipeline, other running\n                                    jobs will be killed.\n                                     - retry: Retry this job on the scheduler\n                                    system.\n                                    Default: <from config>\n  --num_retries <INT>             - How many times to retry the job when failed.\n                                    Default: <from config>\n  --forks <INT>                   - How many jobs to run simultaneously by the\n                                    scheduler.\n                                    Default: <from config>\n  --submission_batch <INT>        - How many jobs to submit simultaneously to\n                                    the scheduler system.\n                                    Default: <from config>\n  --workdir <PATH>                - The workdir for the pipeline.\n                                    Default: <from config>\n  --scheduler <STR>               - The default scheduler.\n                                    Default: <from config>\n  --scheduler_opts <JSON>         - The default scheduler options. Will update\n                                    to the default one.\n                                    Default: <from config>\n  --plugins <LIST>                - A list of plugins to only enabled or\n                                    disabled for this pipeline.\n                                    To disable plugins, use no:<plugin_name>\n                                    Default: <from config>\n  --plugin_opts <JSON>            - Plugin options. Will update to the default.\n                                    Default: <from config>\n  --template_opts <JSON>          - Template options. Will update to the\n                                    default.\n                                    Default: <from config>\n  --outdir <PATH>                 - The output directory for the pipeline.\n                                    Default: <from config>\n  -h, --help                      - Print help information for this command\n```\n\nSee more examples in `examples/` folder.\n\n[1]: https://github.com/pwwang/pipen\n",
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pipen-args',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
