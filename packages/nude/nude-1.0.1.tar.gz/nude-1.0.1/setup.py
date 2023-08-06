from setuptools import setup, find_packages
from sys import platform
from distutils.command.install import install
class Setup(install):
    def run(self):
        install.run(self)
        from nude.setup import setup
        setup()
setup(
    name='nude',
    version='1.0.1',
    license='MIT',
    author='Elisha Hollander',
    author_email='just4now666666@gmail.com',
    description="Turn clothed women nude",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/nude',
    project_urls={
        'Documentation': 'https://github.com/donno2048/nude#readme',
        'Bug Reports': 'https://github.com/donno2048/nude/issues',
        'Source Code': 'https://github.com/donno2048/nude',
    },
    python_requires='>=3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.txt").read().split("\n"),
    dependency_links=[None if platform == "win32" else "https://download.pytorch.org/whl/torch_stable.html"],
    classifiers=['Programming Language :: Python :: 3'],
    entry_points={ 'console_scripts': [ 'nude-cli=nude.__main__:cli', 'nude-gui=nude.__main__:gui' ] },
    cmdclass={'install': Setup}
)
