from setuptools import setup, find_packages

setup(
    name='mymymy',
    version='0.0.1',
    description='my test',
    author='ZD',
    author_email='995084571@qq.com',
    py_modules=["mymymy"],
    packages=['mymymy'],
    license='MIT',
    platform='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['pandas', 'numpy']
)