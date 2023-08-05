Welcome to {{ base.pkg_full_name }}'s documentation!
====================================================

.. toctree::
   :caption: Contents
   :maxdepth: 2

   readme
   installation
   usage
   management

.. toctree::
   :caption: User's documentation
   :maxdepth: 2

   user/index
{%- if sphinx.gallery != "" %}
   _gallery/index{% endif %}

.. toctree::
   :caption: Developer's documentation
   :maxdepth: 4

   Sources <_dvlpt/modules>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
