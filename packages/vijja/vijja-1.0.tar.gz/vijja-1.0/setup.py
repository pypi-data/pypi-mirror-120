from setuptools import setup, find_packages

classifier = [
    'Development Status :: Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Windows 10 :: Kali Lunux',
    'License :: MIT License',
    'Programming Language :: Python3'

]

setup(
    name='vijja',
    version='1.0',
    description='Only For Education Purpose',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='winhtut',
    author_email='winhtutonline@gmail.com',
    license='MIT',
    classifier=classifier,
    keyword='',
    packages=find_packages(),
    install_requires=['paramiko', 'termcolor', 'playsound']  # external packages as dependencies
)
