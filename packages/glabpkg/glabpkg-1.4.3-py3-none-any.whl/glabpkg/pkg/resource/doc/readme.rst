Overview
========

.. {# pkglts, glabpkg
{% for badge in doc.badges -%}
{{ badge }}
{% endfor %}

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

{{ doc.description }}
