.. _development:

===========================
Local Development & Testing
===========================

Local development is largely done with pipenv_. Install the project once
to get all necessary dependencies.

.. code:: bash

    $ cd django-staticinline/

    $ pip install pipenv  # If you don't have pipenv yet

    $ pipenv install --dev

You can test the code against all currently support versions of Django and Python
with tox_ by simply running ``tox`` in the project directorty:

.. code:: bash

    $ pipenv run tox


A quicker way is to test the app against your current Django/Python version with
pipenv directly:

.. code:: bash

    $ pipenv run test


If you want to extend the documentation, you can compile it using pipenv as well:

.. code:: bash

    $ pipenv run docs        # Compiles it once

    $ pipenv run watch-docs  # Keeps a runserver-like process in the background,
                             # which compiles the docs on every file save.

.. _tox: https://tox.readthedocs.io/en/latest/
.. _pipenv: https://docs.pipenv.org/