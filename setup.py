from setuptools import find_packages, setup

setup(
    name='src',
    version='1.0',
    description='对演讲稿数据库的简单运用',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'requests>=2.9.1',
        'flask>=1.0.2'
    ]
)