============
Coding style
============

Framework style
===============

Please follow these coding standards when writing code for inclusion in Django:

    * Unless otherwise specified, follow `PEP 8`_.

      You could use  a tool like `pep8.py`_ to check for some problems in this
      area, but remember that PEP 8 is only a guide, so respect the style of
      the surrounding code as a primary goal.

    * Use four spaces for indentation.

    * Use underscores, not camelCase, for variable, function and method names
      (i.e. ``poll.get_unique_voters()``, not ``poll.getUniqueVoters``).

    * Use ``InitialCaps`` for class names (or for factory functions that
      return classes).

    * Mark all strings for internationalization; see the `i18n documentation`_
      for details.

    * In docstrings, use "action words" such as::

          def foo():
              """
              Calculates something and returns the result.
              """
              pass

      Here's an example of what not to do::

          def foo():
              """
              Calculate something and return the result.
              """
              pass

    * Please don't put your name in the code you contribute. Our policy is to
      keep contributors' names in the ``AUTHORS`` file distributed with Fluo
      -- not scattered throughout the codebase itself. Feel free to include a
      change to the ``AUTHORS`` file in your patch if you make more than a
      single trivial change.

Template style
--------------

    * In Django template code, put one (and only one) space between the curly
      brackets and the tag contents.

      Do this::

          {{ foo }}

      Don't do this::

          {{foo}}

View style
----------

    * In Django views, the first parameter in a view function should be called
      ``request``.

      Do this::

          def my_view(request, foo):
              # ...

      Don't do this::

          def my_view(req, foo):
              # ...

Model style
-----------

    * Field attributes should be put one for line, always ending
      with a comma

      Do this::

          class Person(models.Model):
              first_name = models.CharField(
                  max_length=20,
                  verbose_name=_('First name'),
              )
              last_name = models.CharField(
                  max_length=40,
                  blank=Null,
                  null=True,
                  verbose_name=_('Last name'),
              )

      Don't do this::

          class Person(models.Model):
              first_name = models.CharField(max_length=20, verbose_name=_('First name'))
              last_name = models.CharField(
                  verbose_name=_('Last name'),
                  max_length=40
              )

    * The order of field attributes must follow this order, if used

        specific field attributes, as::

            * ForeignKey/ManyToMany class
            * related_name
            * upload_to
            * max_length
            * max_digits
            * decimal_places
            * ...

        all other common attributes::

            * default
            * choices
            * blank
            * null
            * unique
            * core
            * db_index
            * verbose_name
            * help_text

    * Field names should be all lowercase, using underscores instead of
      camelCase.

      Do this::

          class Person(models.Model):
              first_name = models.CharField(
                  max_length=20,
              )
              last_name = models.CharField(
                  max_length=40,
              )

      Don't do this::

          class Person(models.Model):
              FirstName = models.CharField(
                  max_length=20,
              )
              Last_Name = models.CharField(
                  max_length=40,
              )

    * The ``class Meta`` should appear *after* the fields are defined, with
      a single blank line separating the fields and the class definition.

      Do this::

          class Person(models.Model):
              first_name = models.CharField(
                  max_length=20,
              )
              last_name = models.CharField(
                  max_length=40,
              )

              class Meta:
                  verbose_name_plural = _('people')

      Don't do this::

          class Person(models.Model):
              first_name = models.CharField(
                  max_length=20,
              )
              last_name = models.CharField(
                  max_length=40,
              )
              class Meta:
                  verbose_name_plural = _('people')

      Don't do this, either::

          class Person(models.Model):
              class Meta:
                  verbose_name_plural = _('people')

              first_name = models.CharField(
                  max_length=20,
              )
              last_name = models.CharField(
                  max_length=40,
              )

    * Meta fields should follow this order:

        * abstract
        * verbose_name
        * verbose_name_plural
        * ordering
        * unique_together
        * ...

    * The order of model inner classes and standard methods should be as
      follows (noting that these are not all required):

        * All database fields
        * ``class Meta``
        * ``def __unicode__()``
        * ``def __str__()``
        * ``def save()``
        * ``def get_absolute_url()``
        * Any custom methods

    * If ``choices`` is defined for a given model field, define the choices as
      a tuple of tuples, with an all-uppercase name, either near the top of the
      model module or just above the model class. Example::

          GENDER_CHOICES = (
              ('M', 'Male'),
              ('F', 'Female'),
          )

Documentation style
===================

We place a high importance on consistency and readability of documentation.
(After all, Django was created in a journalism environment!)

How to document new features
----------------------------

We treat our documentation like we treat our code: we aim to improve it as
often as possible. This section explains how writers can craft their
documentation changes in the most useful and least error-prone ways.

Documentation changes come in two forms:

    * General improvements -- Typo corrections, error fixes and better
      explanations through clearer writing and more examples.

    * New features -- Documentation of features that have been added to the
      framework since the last release.

Our philosophy is that "general improvements" are something that *all* current
Django users should benefit from, including users of trunk *and* users of the
latest release. Hence, the documentation section on djangoproject.com points
people by default to the newest versions of the docs, because they have the
latest and greatest content. (In fact, the Web site pulls directly from the
Subversion repository, converting to HTML on the fly.)

But this decision to feature bleeding-edge documentation has one large caveat:
any documentation of *new* features will be seen by Django users who don't
necessarily have access to those features yet, because they're only using the
latest release. Thus, our policy is:

    **All documentation of new features should be written in a way that clearly
    designates the features are only available in the Django development
    version. Assume documentation readers are using the latest release, not the
    development version.**

Our traditional way of marking new features is by prefacing the features'
documentation with: "New in Django development version." Changes aren't
*required* to include this exact text, but all documentation of new features
should include the phrase "development version," so we can find and remove
those phrases for the next release.

Guidelines for ReST files
-------------------------

These guidelines regulate the format of our ReST documentation:

    * In section titles, capitalize only initial words and proper nouns.

    * Wrap the documentation at 80 characters wide, unless a code example
      is significantly less readable when split over two lines, or for another
      good reason.

Commonly used terms
-------------------

Here are some style guidelines on commonly used terms throughout the
documentation:

    * **Django** -- when referring to the framework, capitalize Django. It is
      lowercase only in Python code and in the djangoproject.com logo.

    * **e-mail** -- it has a hyphen.

    * **MySQL**

    * **PostgreSQL**

    * **Python** -- when referring to the language, capitalize Python.

    * **realize**, **customize**, **initialize**, etc. -- use the American
      "ize" suffix, not "ise."

    * **SQLite**

    * **subclass** -- it's a single word without a hyphen, both as a verb
      ("subclass that model") and as a noun ("create a subclass").

    * **Web**, **World Wide Web**, **the Web** -- note Web is always
      capitalized when referring to the World Wide Web.

    * **Web site** -- use two words, with Web capitalized.

Django-specific terminology
---------------------------

    * **model** -- it's not capitalized.

    * **template** -- it's not capitalized.

    * **URLconf** -- use three capitalized letters, with no space before
      "conf."

    * **view** -- it's not capitalized.

.. _PEP 8: http://www.python.org/peps/pep-0008.html
.. _pep8.py: http://svn.browsershots.org/trunk/devtools/pep8/pep8.py
.. _i18n documentation: ../i18n/

