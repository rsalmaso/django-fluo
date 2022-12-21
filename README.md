# django-fluo

My personal django reusable stuffs.


## CHANGES ##

### dev

* Drop support for Django < 3.2
* Drop support for Python < 3.8
* Add support for Python 3.9, 3.10, 3.11
* Drop StatusModel as it is not easyly customizable, use StatusField
* Remove `jquery_ajaxqueue` templatetag
* Remove `jquery` templatetag
* Remove `css_ie` templatetag
* Remove `css_print` templatetag
* Enable PEP 563 – Postponed Evaluation of Annotations
* Drop `fluo.forms.fields.JsonField`
* Remove `postgresql_psycopg2` backend
