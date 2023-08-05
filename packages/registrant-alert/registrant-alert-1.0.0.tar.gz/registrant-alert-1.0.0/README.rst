.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: registrant-alert-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/registrant-alert.svg
    :alt: registrant-alert-py release
    :target: https://pypi.org/project/registrant-alert

.. image:: https://github.com/whois-api-llc/registrant-alert-py/workflows/Build/badge.svg
    :alt: registrant-alert-py build
    :target: https://github.com/whois-api-llc/registrant-alert-py/actions

========
Overview
========

The client library for
`Registrant Alert API <https://registrant-alert.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.6.

Installation
============

.. code-block:: shell

    pip install registrant-alert

Examples
========

Full API documentation available `here <https://registrant-alert.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

.. code-block:: python

    from registrantalert import *

    client = Client('Your API key')

Make basic requests
-------------------

.. code-block:: python

    # Get the number of domains.
    terms = {
        'include': ['blog']
    }
    result = client.preview(basic_terms=terms)
    print(result.domains_count)

    # Get raw API response
    raw_result = client.raw_data(
        basic_terms=terms,
        response_format=Client.XML_FORMAT,
        mode=Client.PREVIEW_MODE)

    # Get a list of registered/dropped domains (up to 10,000)
    result = client.purchase(
        basic_terms=terms
    )

Advanced usage
-------------------

Extra request parameters

.. code-block:: python

    advanced_terms = [{
        'field': Fields.registrant_contact_organization,
        'term': 'Airbnb, Inc.',
        'exactMatch': True
    }]
    since_date = datetime.date(2021, 8, 12)
    result = client.purchase(
        advanced_terms=advanced_terms,
        since_date=since_date,
        punycode=False)

Response model overview
-----------------------

.. code-block:: python

    Response:
        - domains_count: int
        - domains_list: [Domain]
            - domain_name: str
            - date: datetime.date
            - action: str

