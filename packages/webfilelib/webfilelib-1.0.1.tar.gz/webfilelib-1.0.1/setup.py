from setuptools import *
from setupargs import *
__version__,__author__="1.0.1","Ruoyu Wang"
setup(

name='webfilelib',

version=__version__,

author=__author__,

author_email='wangruoyu666@outlook.com',

description='上传你的文件到云上',


#long_description_content_type='text/markdown',

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
