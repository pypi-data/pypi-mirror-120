Verlauf - The Terminal Color Gradient Generator
===============================================

.. image:: ./screenshot/screen.jpg

Installation
------------

To install ``verluaf``, simply run

::

    pip install verlauf

Usage
-----

::

    verlauf [start] [end] [steps]


Examples
--------

::

    $ verlauf --help
    Usage: gradients.py [OPTIONS] START END [STEPS]

      Generates a gradient from START to END STEPS long (ends inclusive)

    Options:
      --help  Show this message and exit.
    $ verlauf f00 00f           # This produces 5 colors between #ff0000 and #0000ff
    $ verlauf '#0abc0d' abcdef  # '#' in color names are optional
    $ verlauf 0abc0d abcdef 7   # This will produce 7 colors in between

