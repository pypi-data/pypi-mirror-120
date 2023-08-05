ATOM V1 -> RSS V2
=================

The project produces RSS2 file from Atom file. It provides an XSL
stylesheet (V2) for this purpose.

Informations and validator about Atom format : `validator.w3.org for
Atom <https://validator.w3.org/feed/docs/atom.html>`__

Informations and validator about RSS2 format : `validator.w3.org for
RSS2 <https://validator.w3.org/feed/docs/rss2.html>`__

XSL stylesheet
--------------

Assumptions for the **XSL** transformation (with an `XSLT
2 <https://www.w3.org/TR/xslt20>`__ processor): - Atom feed is valid
without warning - RSS2 feed will be valid without warning - Atom feed is
named ``feedname.xml`` - RSS2 feed will be named ``feedname.rss2`` (only
the extension is changed in the self link inside the content) - Use XSLT
v2 to format date `RFC 822 <http://www.faqs.org/rfcs/rfc822.html>`__

Python
------

The small component ``xslt_ext.py`` takes the XSLT v2 stylesheet and
makes some tweaks. The `lxml
package <https://pypi.python.org/pypi/lxml>`__ only supports XSLT v1
transformations.

Then the call to the XSLT 2 function
```format-dateTime`` <https://www.w3.org/TR/xslt20/#format-date>`__
isn’t possible.

As a result, the component : - defines 1 new XSL that imports the
original (XSL v2) and produce an XSL v1 stylesheet - defines a python
extension to convert the dates from ISO format (used in Atom) to RFC 822
format (used in RSS2) - replaces the XSL template calling
``format-dateTime`` by an XSL template calling python function - makes
the transformation in XSLT 1

Code to makes the XSL transformation in python :

::

   proc = xslt_ext.DateFormatterProcessor()
   proc.load_xslt(xslt_filename) # defaut=atom1_to_rss2_pyext.xsl
   result_xml = proc.transform(etree.parse(atom_filename))

Program to convert atom feed into rss feed : ``atom1_to_rss2.py``

::

   $ python atom1_to_rss2.py --help

   usage: atom1_to_rss2.py [-h] [--atom ATOM] [--rss2 RSS2] [--xslt XSLT]

   optional arguments:
     -h, --help   show this help message and exit
     --atom ATOM  Atom filename (input)
     --rss2 RSS2  RSS2 filename (output)
     --xslt XSLT  XSLT stylesheet (optionnal), default=atom1_to_rss2_pyext.xsl

# Licence `MIT <LICENSE>`__
