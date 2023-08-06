# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_filehost']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0', 'nonebot2>=2.0.0-alpha.15,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-filehost',
    'version': '0.1.0',
    'description': 'A HTTP static file hosting plugin for NoneBot2, which provides an graceful solution for cross-machine file transfer.',
    'long_description': '# nonebot-plugin-filehost\n\n> **NoneBot2 的 HTTP 静态文件托管插件，为跨机文件传输提供了优雅的解决方案**\n\n---\n\n## 优势\n\n- 跨机器, 跨网络支持, 只要反向WebSocket可以正常连接, 它就可以使用\n\n- 使用临时文件作为中转, 内存占用低\n  - 临时文件会尝试采用硬链接方式创建, 快速且可靠\n  - 临时文件在程序退出时会自动删除, 不会永久占用空间\n  \n- 自动检测访问来源生成资源URL, 无需手动配置\n\n## 开始使用\n\n### 安装插件\n\n- 如果使用了`nb-cli`\n\n```shell\nnb plugin install nonebot-plugin-filehost\n```\n\n- 或者手动安装:\n\n  - 使用你的包管理器(如`pip`)安装`nonebot-plugin-filehost`:\n\n    ```shell\n    pip install nonebot-plugin-filehost\n    ```\n\n  - 修改`pyproject.toml`文件(推荐)\n\n    ```diff\n    [nonebot.plugins]\n    - plugins = []\n    + plugins = ["nonebot_plugin_filehost"]\n    plugin_dirs = ["src/plugins"]\n    ```\n\n  - 修改`bot.py`文件, 添加一行:\n  \n    ```diff\n    driver = nonebot.get_driver()\n    driver.register_adapter("cqhttp", CQHTTPBot)\n\n    nonebot.load_from_toml("pyproject.toml")\n    + nonebot.load_plugin(\'nonebot_plugin_filehost\')\n    ```\n\n### 使用插件\n\n- 请前往[示例插件](./src/plugins/testing/__init__.py)进行查看\n\n## 开源许可\n\n本项目采用[MIT许可](./LICENSE)\n',
    'author': 'Mix',
    'author_email': 'mnixry@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mnixry/nonebot-plugin-filehost',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
