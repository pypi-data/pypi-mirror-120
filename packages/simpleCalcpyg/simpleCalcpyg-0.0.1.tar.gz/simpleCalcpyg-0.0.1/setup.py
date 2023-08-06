from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Unix',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='simpleCalcpyg',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='yunes fatahi',
    author_email='panahikaren91@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    #if your package has libs that it uses you may want to specify them here so that they are automaticly ddownloaded by the same pip command
    packages=find_packages(),
    install_requires=['']
)


