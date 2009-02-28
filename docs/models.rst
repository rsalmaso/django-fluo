===============
DataBase Fields
===============


``Fluo`` defines some generic fields


StatusField
===========

A CharField, with default settings:

    * ``choices`` -- a tuple with `'active'`, `'inactive'`
    * ``max_length`` -- set to `10` characters
    * ``default`` -- `'active'`
    * ``verbose_name`` -- `'status'`
    * ``help_text`` -- `'Is active?'`


===============
DataBase Models
===============


``Fluo`` defines some abstract models


OrderedModel
============

``OrderedModel`` has these field:

    * ordering -- Optional.

and these methods:

    * ``brothers_and_me()`` -- Returns all siblings and the objects itself
    * ``brothers()`` -- Returns all siblings without self
    * ``is_first()`` -- Returns if the object is the first one
    * ``is_last()`` -- Returns if the object is the last one
    * ``up()`` -- Move up the object, and push down all others
    * ``down()`` -- Move down the object, and push up all others

TreeOrderedModel
================

``TreeOrderedModel`` derives from OrderedModel, and it has these field:

    * parent -- Optional. The parent node. A ``ForeignKey`` to ``TreeOrderedModel``

