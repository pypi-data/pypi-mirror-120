from setuptools import setup, find_packages

__author__="Ruoyu Wang"
__version__="0.0.1"

# read the contents of your README file

from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:

    long_description = f.read()

setup(

name='guiMaker',

version=__version__,

author=__author__,

author_email='wangruoyu666@outlook.com',

description='一个简单易用的GUI创建库。',

#long_description=long_description,

long_description_content_type='text/markdown',

classifiers=[

'Development Status :: 4 - Beta',

'Intended Audience :: Developers',

'Topic :: Software Development :: Libraries',

'Programming Language :: Python :: 3',

# 省略一下

],

packages=find_packages(),

python_requires='>=3.5',

install_requires=[],

project_urls={
'Source': 'https://github.com/ruanima/dingtalk-log-handler',

},

)
''''————————————————
版权声明：本文为CSDN博主「weixin_39611275」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_39611275/article/details/113641108'''