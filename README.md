# PYLANTIR

## Description

This is a Python package for KI engineering.
It consists of:

- PyElbe: a Python package for hand calculation.
- PyWeser: a Python package for ISAMI interface.
- PyLech: a package for FE analysis and interfacing.

## Installation

### Requirements

- Python 3.10 or higher
- numpy
- matplotlib

### Install

from the airbus artifactory:

```bash
pip install pylantir
```

## Documentation

Documentation is made automatically using Sphinx and can be found [here](https://TODO:-airbus-mock-address/pylantir/).

Automatically updating the documentation is done in the CI/CD pipeline using the make.bat command
 and jenkins.

When the package is extended, run the following command to update the documentation rst files:

```bash
sphinx-apidoc -f -o docs/source/ pylantir
```

### Sphinx tips

#### Add pictures
you can add pictures in the documentation by adding the image to the docs/source/_static folder and
 using the following syntax in the rst file:

```php
.. image:: ./_static/your_image.png
    :width: 100%
    :align: center
    :alt: alternative text
```

#### Inline math
you can add inline LaTeX by using the following syntax:
(online LaTeX equasion editor: https://www.codecogs.com/eqneditor/editor.php)

```php
:math:`\frac{1}{2}`
```
