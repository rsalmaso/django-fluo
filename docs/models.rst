===============
DataBase Fields
===============


``Fluo`` defines some generic fields


StatusField
===========

A CharField, with default settings:

    * choices -- a tuple with `'active'`, `'inactive'`
    * max_length -- set to `10` characters
    * default -- `'active'`
    * verbose_name -- `'status'`
    * help_text -- `'Is active?'`

