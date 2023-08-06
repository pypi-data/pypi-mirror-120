from setuptools import setup, find_packages

setup(name='mminepy', # 패키지 명

version='1.0.0.5',

description='minepy from elbert06',

author='elbert06',

author_email='elbert06@hanmail.net',


license='MIT', # MIT에서 정한 표준 라이센스 따른다

py_modules=['mminepy'], # 패키지에 포함되는 모듈

python_requires='>=3',

install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

packages=['mminepy'] # 패키지가 들어있는 폴더들

)