pywkher
==========

wkhtmltopdf_ is a command line program that converts HTML to PDF using
the WebKit rendering engine, as provided by Qt_.  Because it uses WebKit,
you can use wkhtmltopdf to generate screenshots, or generate PDFs from
Django or Rails or whatever, and the resulting PDFs will look awesome.

The typical install process includes downloading and compiling Qt,
followed by downloading and installing wkhtmltopdf.

But you can't really download and compile packages inside a Heroku_
dyno, so you need to vendor in any external binaries you might want to use
(that aren't Python packages that compile themselves).  This package
provides a simple way to include and use a wkhtmltopdf binary that has
been compiled for the Heroku (Cedar stack) dyno environment.

.. _Heroku: http://www.heroku.com/
.. _wkhtmltopdf: http://code.google.com/p/wkhtmltopdf/
.. _Qt: http://qt.nokia.com/products/

Installation
------------

Install it in the usual way::

    pip install pywkher

Usage
-----

One easy way of using wkhtmltopdf in your Python program is to use the
included ``generate_pdf`` command.  The ``generate_pdf`` command takes either a
URL or an HTML document and returns a Python NamedTemporaryFile object
referencing the generated PDF (which will be stored in the Heroku instance's
temporary directory).

Here's an example of using the ``generate_pdf`` command to render a Django template
as a PDF and return the resulting PDF as part of the HTTP response::

  from os.path import basename
  from wsgiref.util import FileWrapper

  from django.http import HttpResponse
  from django.template import RequestContext
  from django.template.loader import get_template

  from pywkher import generate_pdf


  def return_a_pdf(request):
    template = get_template('my_awesome_template.html')
    html = template.render(RequestContext(request))
    pdf_file = generate_pdf(html=html)
    response = HttpResponse(FileWrapper(pdf_file), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % basename(pdf_file.name)
    response['Content-Length'] = pdf_file.tell()
    pdf_file.seek(0)
    return response


Usage in Development
--------------------

If you want to test your app locally, obviously the binary that's compiled
for Heroku isn't going to work, unless your development or test environment
closely mimics Heroku's.  However, the ``generate`` function will look for
an environment variable named ``WKHTMLTOPDF_CMD`` and will only use the
internally-bundled wkhtmltopdf binary if that environment variable is not set.

Therefore, if you're on a Mac, do something like:

- ``brew install wkhtmltopdf`` (Homebrew_ required for this)

- ``export WKHTLMTOPDF_CMD=wkhtmltopdf``

- ``python my_python_program.py`` (just an example)

.. _Homebrew: http://mxcl.github.com/homebrew/

Acknowledgements
----------------

Brad Phelan generated the binary that's included here as part of his
wkhtmltopdf-heroku_ gem.  It's thanks to his efforts that I didn't have
to go through the whole Heroku vulcan build process myself.

.. _wkhtmltopdf-heroku: https://github.com/bradphelan/wkhtmltopdf-heroku
