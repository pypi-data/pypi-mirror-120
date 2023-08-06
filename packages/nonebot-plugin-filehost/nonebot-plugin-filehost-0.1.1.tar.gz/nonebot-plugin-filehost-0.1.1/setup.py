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
    'version': '0.1.1',
    'description': 'A HTTP static file hosting plugin for NoneBot2, which provides an graceful solution for cross-machine file transfer.',
    'long_description': '# nonebot-plugin-filehost\n\n> **NoneBot2 的 HTTP 静态文件托管插件，为跨机文件传输提供了优雅的解决方案**\n\n[![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-filehost?style=for-the-badge)](https://pypi.org/project/nonebot-plugin-filehost/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonebot-plugin-filehost?style=for-the-badge)\n\n[![GitHub issues](https://img.shields.io/github/issues/mnixry/nonebot-plugin-filehost)](https://github.com/mnixry/nonebot-plugin-filehost/issues)\n[![GitHub stars](https://img.shields.io/github/stars/mnixry/nonebot-plugin-filehost)](https://github.com/mnixry/nonebot-plugin-filehost/stargazers)\n[![GitHub forks](https://img.shields.io/github/forks/mnixry/nonebot-plugin-filehost)](https://github.com/mnixry/nonebot-plugin-filehost/network)\n[![GitHub license](https://img.shields.io/github/license/mnixry/nonebot-plugin-filehost)](https://github.com/mnixry/nonebot-plugin-filehost/blob/main/LICENSE)\n![Lines of code](https://img.shields.io/tokei/lines/github/mnixry/nonebot-plugin-filehost)\n\n---\n\n## 优势\n\n- 跨机器, 跨网络支持, 只要反向WebSocket可以正常连接, 它就可以使用\n\n- 使用临时文件作为中转, 内存占用低\n  - 临时文件会尝试采用硬链接方式创建, 快速且可靠\n  - 临时文件在程序退出时会自动删除, 不会永久占用空间\n  \n- 自动检测访问来源生成资源URL, 无需手动配置\n\n## 开始使用\n\n### 安装插件\n\n- 如果使用了`nb-cli`\n\n```shell\nnb plugin install nonebot-plugin-filehost\n```\n\n- 或者手动安装:\n\n  - 使用你的包管理器(如`pip`)安装`nonebot-plugin-filehost`:\n\n    ```shell\n    pip install nonebot-plugin-filehost\n    ```\n\n  - 修改`pyproject.toml`文件(推荐)\n\n    ```diff\n    [nonebot.plugins]\n    - plugins = []\n    + plugins = ["nonebot_plugin_filehost"]\n    plugin_dirs = ["src/plugins"]\n    ```\n\n  - 修改`bot.py`文件, 添加一行:\n  \n    ```diff\n    driver = nonebot.get_driver()\n    driver.register_adapter("cqhttp", CQHTTPBot)\n\n    nonebot.load_from_toml("pyproject.toml")\n    + nonebot.load_plugin(\'nonebot_plugin_filehost\')\n    ```\n\n### 使用插件\n\n- 请前往[示例插件](./src/plugins/testing/__init__.py)进行查看\n\n### 进行配置\n\n本插件支持以下配置项\n\n- `FILEHOST_FALLBACK_HOST`\n  - 当请求不包含`Host`头或者上下文变量序列化失败时使用的主机地址\n  - 默认为`None`, 示例值为`http://localhost:8080`\n  \n- `FILEHOST_LINK_FILE`\n  - 使用文件系统链接代替文件复制, 可以提升临时文件创建速度\n  - 默认为`True`,同时支持`bool`和`int`类型\n    - 当为`bool`时, 无条件启用链接\n    - 当为`int`时, 当文件字节数大于或等于该数时启用链接, 低于时使用复制\n\n- `FILEHOST_LINK_TYPE`\n  - 指定使用的链接类型, 有`hard`和`soft`两个可选值\n    - `hard`: 建立硬链接\n    - `soft`: 链接软链接 (符号链接)\n  - 默认为`hard`\n\n## 开源许可\n\n本项目采用[MIT许可](./LICENSE)\n',
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
