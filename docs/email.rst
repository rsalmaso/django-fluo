==============
Sending emails
==============

:class:`~fluo.utils.mail.EmailMessage`
======================================

**Description:**

``Fluo`` :class:`~fluo.utils.mail.EmailMessage` improves the original :class:`~django.utils.mail.EmailMessage`:
it adds a `Cc` header and accepts a single argument for ``to``, ``cc`` and ``bcc`` parameters instead of list or tuple
with only one element.

**Aruments:**

    * ``subject``: the subject of the email

    * ``body``: the body text

    * ``from_email``: the sender's address

    * ``to``: a string, a list or a tuple of recipient list

    * ``cc``: a string, a list or a tuple of addresses used in 'Cc' header when sending the e-mail

    * ``bcc``: a string, a list or a tuple of addresses used in 'Bcc' header when sending the e-mail

    * ``connection``: a ``SMTPConnection`` instance. Use this parameter if you want to use the
      same connection for multiple messages. If omitted, a new connection is created when
      ``send()`` is called.

    * ``attachments``: a list of attachments to put on the message. These can be either ``email.MIMEBase.MIMEBase``
      instance, or ``(filename, content, mimetype)`` triples.

    * ``headers``: a dictionary of extra headers to put on the message. The keys are the header name,
      values are the header values. It's up to the caller to ensure header names and values are in the
      correct format for an e-mail message.

**Example:**

Create a mail message::

    mail = EmailMessage(
        subject='Hello',
        body='Body goes here',
        from_email='alert@example.com',
        to=['bob@example.com',],
        cc=['alice@example.com', 'ted@example.com',],
        bcc='chief@example.com',
        headers={'Reply-To': 'devnull@example.com'},
    )

:class:`~fluo.utils.mail.EmailMultiAlternatives`
================================================

This class acts exactly as :class:`~django.core.mail.EmailMultiAlternatives`,
but inherits :class:`~fluo.utils.mail.EmailMessage`.

