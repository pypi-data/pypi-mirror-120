# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vhrun3',
 'vhrun3.app',
 'vhrun3.app.routers',
 'vhrun3.builtin',
 'vhrun3.ext',
 'vhrun3.ext.har2case',
 'vhrun3.ext.locust',
 'vhrun3.ext.uploader',
 'vhrun3.report',
 'vhrun3.report.html']

package_data = \
{'': ['*']}

install_requires = \
['httprunner>=3.1.6,<4.0.0']

entry_points = \
{'console_scripts': ['vhar2case = vhrun3.cli:main_har2case_alias',
                     'vhmake = vhrun3.cli:main_make_alias',
                     'vhrun = vhrun3.cli:main_hrun_alias',
                     'vhrun3 = vhrun3.cli:main',
                     'vlocusts = vhrun3.ext.locust:main_locusts']}

setup_kwargs = {
    'name': 'vhrun3',
    'version': '1.0.1',
    'description': '',
    'long_description': '    基于httprunner==3.1.6版本，根据特定需求二次定制开发\n    \n    1、保留2.x版本的用例分层机制，避免冗余出现api基本信息（url、headers、method等）\n    2、除支持http和https协议外，支持SSH协议，可以远程执行shell命令、文件上传和下载\n    3、兼容支持2.x测试报告，便于测试时调试\n    4、数据驱动改成一个Class N个test_*用例方式，便于用例扫描\n    5、支持test_xx的__doc__自动生成，并支持config.variables和parameters变量解析\n    6、yml中config中usefixtures字段，支持pytest指定添加fixture\n\n    参考：\n    homepage = "https://github.com/httprunner/httprunner"\n    repository = "https://github.com/httprunner/httprunner"\n    documentation = "https://docs.httprunner.org"\n    blog = "https://debugtalk.com/',
    'author': 'tigerjlx',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
