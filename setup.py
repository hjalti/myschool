from distutils.core import setup

setup(
    name='MyschoolScraper',
    version='0.1.2',
    author='Hjalti Magnússon',
    author_email='hjaltmann@gmail.com',
    packages=['myschool'],
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='',
    long_description='',
    install_requires=[
        "requests >= 2.3.0",
        "beautifulsoup4 >= 4.3.2",
    ],
)

