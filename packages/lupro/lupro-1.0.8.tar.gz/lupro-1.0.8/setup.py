from distutils.core import setup
from setuptools import find_packages

from lupro import lupro
setup(name='lupro',  # 包名
      version='1.0.8',  # 版本号
      description='Elegant reptile frame for python.',
      long_description='https://github.com/luxuncang/lupro',
      author='ShengXin Lu',
      author_email='luxuncang@qq.com',
      url='https://github.com/luxuncang/lupro',
      install_requires=['gevent','requests','lxml','dtanys','decorator','chardet','parsel','httpx'],
      license='MIT',
      packages=find_packages(),
      include_package_data = True,
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )