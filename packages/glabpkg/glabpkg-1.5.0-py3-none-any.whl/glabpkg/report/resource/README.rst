.. {# pkglts, glabreport, after doc
main: |main_build|_ |main_coverage|_

.. |main_build| image:: {{ gitlab.url }}/badges/main/pipeline.svg
.. _main_build: {{ gitlab.url }}/commits/main

.. |main_coverage| image:: {{ gitlab.url }}/badges/main/coverage.svg
.. _main_coverage: {{ gitlab.url }}/commits/main


prod: |prod_build|_ |prod_coverage|_

.. |prod_build| image:: {{ gitlab.url }}/badges/prod/pipeline.svg
.. _prod_build: {{ gitlab.url }}/commits/prod

.. |prod_coverage| image:: {{ gitlab.url }}/badges/prod/coverage.svg
.. _prod_coverage: {{ gitlab.url }}/commits/prod
.. #}

Instructions
------------

To compile the documentation, you need a python environment with sphinx.

.. code-block:: bash

    $ conda activate myenv
    (myenv)$ cd report
    (myenv)$ make html

The resulting document should be in **report/build/html/index.html**

If you want to replay the analysis, all the scripts that generated the figures
are in the **script** folder.
