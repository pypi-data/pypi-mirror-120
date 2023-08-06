===========
Slack Forms
===========

Forms icing on the Slack cake

Dev Setup
---------
::

    pipenv install --dev

Lint and Test
-------------
::

    pipenv run make lint test

Package
-------
::

    pipenv run make dist

Run Sample App
--------------
::

    cp env.sample .env
    vi .env
    pipenv run python -m sample_app.app

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
