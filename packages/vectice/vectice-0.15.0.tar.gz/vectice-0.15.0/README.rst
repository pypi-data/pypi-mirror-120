vectice-python
==============

Python library for Vectice project.

Developer's Setup
-----------------

1. Installation
~~~~~~~~~~~~~~~

It is recommended to install this library in a `virtualenv`_ using pip.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/

Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^

Python >= 3.6

Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    venv/bin/pip install -e .[dev]

if using **Zsh**, add backslash (\\) to escape square brackets:

.. code-block:: console

    venv/bin/pip install -e .\[dev\]

Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv venv
    venv\Scripts\activate
    venv\Scripts\pip.exe install -e .[dev]


2. Start Backend Server
~~~~~~~~~~~~~~~~~~~~~~~

The backend server and database need to be running to receive requests from the Python library. See the `backend`_ repository for more details.

.. _`backend`: https://github.com/vectice/backend

Make sure there exist at least one workspace and one project.

3. Prepare an ApiKey
~~~~~~~~~~~~~~~~~~~~

Go to the GraphQL Playground: http://localhost:4000/graphql

Note that an authentication header is required to perform the following mutations.

Generate an ApiKey
^^^^^^^^^^^^^^^^^^^

.. code-block::

    mutation {
      generateApiKey(workspaceId: 1, apiKey: {name: "Key1"}) {key}
    }

Be sure to save the key somewhere, for it will only show once.

Deploy the ApiKey
^^^^^^^^^^^^^^^^^

.. code-block::

    mutation {
      updateApiKey(workspaceId: 1, apiKeyId: 1, apiKey: {status: DEPLOYED}) {name, status}
    }

4. Example Usage
~~~~~~~~~~~~~~~~

Now, try to run some code in a Python console:

.. code-block:: console

    python -i

.. code-block:: python

    from vectice import Vectice
    vectice = Vectice(project_token="xcvbn")
    vectice.list_jobs()

5. Linting
~~~~~~~~~~

Two linters are used cooperatively in this project, namely `black`_ and `flake8`_. They will be run upon commits (pre-commit hooks) and pull requests (CI).

Commands to run them:

.. code-block:: console

    black .
    flake8

It is recommended to run `black`_ first, then `flake8`_.

.. _`black`: https://black.readthedocs.io/en/stable/
.. _`flake8`: https://flake8.pycqa.org/en/latest/

6. Build
~~~~~~~~

A build step is included in CI. To locally build:

.. code-block:: console

    pip install build
    python -m build
