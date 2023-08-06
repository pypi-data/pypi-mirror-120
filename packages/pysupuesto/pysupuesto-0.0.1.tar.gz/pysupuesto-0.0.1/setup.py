from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Modulo para trabajar con la información presupuestaria pública Argentina'
LONG_DESCRIPTION = 'Modulo que permite descargar series temporales de recursos y el crédito y su ejecución del sitio https://www.presupuestoabierto.gob.ar/sici/datos-abiertos'

# Setting up
setup(
    name="pysupuesto",
    version=VERSION,
    author="@mato",
    author_email="no@mail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'presupuesto', 'administracion publica', 'argentina', 'public budget', 'presupuesto publico'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
