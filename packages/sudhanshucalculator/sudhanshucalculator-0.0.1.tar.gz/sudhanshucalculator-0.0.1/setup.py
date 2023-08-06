from setuptools import setup, find_packages

classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3 ',
        'License :: OSI Approved :: MIT License'
]   
setup(
    name='sudhanshucalculator',
    version='0.0.1',
    author='sudhanshu',
    author_email='sudhanshu.vainayak@gmail.com',
    packages=find_packages(),
    url='',
    download_url='',
    license='MIT',
    description='Scientific measurement library for instruments, experiments, and live-plotting',
    long_description=open('README.txt').read() + "\n\n" + open('CHANGEBLOG.txt').read(),
    install_requires=[''],
    classifiers=classifiers,
    keywords='calculator'
)