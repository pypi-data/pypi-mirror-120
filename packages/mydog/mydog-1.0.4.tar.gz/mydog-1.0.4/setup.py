from setuptools import setup, find_packages

setup(
    name='mydog',
    version='1.0.4',
    packages=find_packages(),
    install_requires=['click', "termcolor"],
    description='prints the contents of the file',
    author='Brijesh krishna',
    author_email='brijesh.krishna@gmail.com',
    long_description_content_type='text/markdown',
    long_description =open('README.md').read(),
    url='https://github.com/Brijeshkrishna/mydog',
    entry_points='''
        [console_scripts]
        mydog=mydog.mydog:dog
    ''',
    keywords=['mydog','cat','dog','console print','python print','python','colour print'],
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
