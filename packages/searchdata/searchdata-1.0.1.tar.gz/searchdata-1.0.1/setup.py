from setuptools import setup

setup(
    name='searchdata',
    version="1.0.1",
    url='https://github.com/SearchDataAPI/python-sdk',
    description='Searchdata Python SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sorin-Gabriel Marica',
    author_email='sorin.marica@jeco.dev',
    maintainer='searchdata',
    maintainer_email='account@jeco.dev',
    license='MIT',
    packages=['searchdata'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
)