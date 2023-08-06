from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='calculaHashDadosAbertos',
    version='0.0.4',
    url='https://github.com/masuta16/calculaHash',
    license='MIT License',
    author='Israel Andrade',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='israndade16@hotmail.com',
    keywords='Pacote',
    description=u'Retorna dados de hash dos ultimos n dias da biblioteca de dados abertos do governo',
    packages=['calculaHashDadosAbertos'],
    install_requires=['requests','pandas','datetime'],)

