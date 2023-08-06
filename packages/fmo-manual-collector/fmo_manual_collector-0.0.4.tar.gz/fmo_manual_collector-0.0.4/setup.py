
from setuptools import setup, find_packages

setup(
    name='fmo_manual_collector',
    version='0.0.4',
    description='Collect FMO from EDGAR filinigs',
    url='https://github.com/exilespacer/fmo_manual_collector',
    author='Chia-Yi Yen',
    author_email='yen.chiayi@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=['fmo_manual_collector'],
    keywords=['fmo', "edgar"],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ]
)