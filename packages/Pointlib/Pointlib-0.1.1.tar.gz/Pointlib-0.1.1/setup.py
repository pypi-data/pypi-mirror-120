from setuptools import find_packages, setup

setup(
    name='Pointlib',
    packages=find_packages(include=['Pointlib']),
    version='0.1.1',
    description='Pointlib create for manage point-coordinate in Python code.',
    author='Chayoot Kosiwanich',
    author_email='khunfloat@gmail.com',
    url='https://github.com/khunfloat/Pointlib',
    download_url='https://github.com/khunfloat/Pointlib/archive/refs/tags/v_0.1.1.tar.gz',
    keywords=['point', 'coordinate'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3',      
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',],
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)