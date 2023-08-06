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
['httprunner>=3.1.6,<4.0.0', 'paramiko==2.6.0']

entry_points = \
{'console_scripts': ['vhar2case = vhrun3.cli:main_har2case_alias',
                     'vhmake = vhrun3.cli:main_make_alias',
                     'vhrun = vhrun3.cli:main_hrun_alias',
                     'vhrun3 = vhrun3.cli:main',
                     'vlocusts = vhrun3.ext.locust:main_locusts']}

setup_kwargs = {
    'name': 'vhrun3',
    'version': '1.1.5',
    'description': '',
    'long_description': '\n#### 介绍\n```\n基于httprunner==3.1.6版本，根据特定需求二次定制开发\n\n1、保留2.x版本的用例分层机制，避免冗余出现api基本信息（url、headers、method等）\n2、除支持http和https协议外，支持SSH协议，可以远程执行shell命令、文件上传和下载\n3、兼容支持2.x测试报告，便于测试时调试\n4、数据驱动改成一个Class N个test_*用例方式，便于用例扫描成独立用例\n5、支持test_xx的__doc__自动生成，并支持config.variables和parameters变量解析\n6、yml中config中usefixtures字段，支持pytest指定添加fixture\n7、支持特定场景下的skipif代码生成\n```\n\n#### 新增SSH部分示例：\n###### 1、执行shell命令\n```\nconfig:\n  name: demo - exec shell cmd\n  variables:\n    executor: ls\n    params: -alh\nteststeps:\n  - name: api -> shell\n    protocol: ssh\n    connection:   # 指定目标机器IP、Port、User和Password\n      ssh_ip: ${ENV(hostname)}  \n      ssh_port: ${ENV(ssh_port)}\n      ssh_user: ${ENV(ssh_user)}\n      ssh_password: ${ENV(ssh_password)}\n    request:\n      type: shell   # 指定类型为执行Shell命令\n      executor: $executor  # shell自带命令或可执行程序\n      params: $params # 字符串或字符串列表\n```\n###### 2、文件上传\n```\nconfig:\n  name: demo - upload file\nteststeps:\n  - name: api -> upload\n    protocol: ssh\n    connection:\n      ssh_ip: ${ENV(hostname)}\n      ssh_port: ${ENV(ssh_port)}\n      ssh_user: ${ENV(ssh_user)}\n      ssh_password: ${ENV(ssh_password)}\n    request:\n        type: upload # 指定类型为文件上传\n        local_path: $local_path  # 相对于本项目根目录的路径\n        remote_path: $remote_path  # 远程绝对路径\n```\n\n###### 3、文件下载\n```\nconfig:\n  name: demo - download file\nteststeps:\n  - name: api -> download\n    protocol: ssh\n    connection:\n      ssh_ip: ${ENV(hostname)}\n      ssh_port: ${ENV(ssh_port)}\n      ssh_user: ${ENV(ssh_user)}\n      ssh_password: ${ENV(ssh_password)}\n    request:\n        type: download # 指定类型为文件下载\n        local_path: $local_path  # 相对于本项目根目录的路径\n        remote_path: $remote_path  # 远程绝对路径\n```\n#### 参考：\n```\nhomepage = "https://github.com/httprunner/httprunner"\nrepository = "https://github.com/httprunner/httprunner"\ndocumentation = "https://docs.httprunner.org"\nblog = "https://debugtalk.com/\n```\n',
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
