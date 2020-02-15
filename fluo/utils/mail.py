# Copyright (C) 2007-2020, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django.core import mail


class EmailMessage(mail.EmailMessage):
    def __init__(
        self,
        subject="",
        body="",
        from_email=None,
        to=None,
        cc=None,
        bcc=None,
        connection=None,
        attachments=None,
        headers=None,
    ):
        if isinstance(to, str):
            to = [to]
        if isinstance(cc, str):
            cc = [cc]
        if isinstance(bcc, str):
            bcc = [bcc]
        self.cc = cc
        super().__init__(subject, body, from_email, to, bcc, connection, attachments, headers)

    def message(self):
        msg = super().message()
        msg["Cc"] = ", ".join(self.cc)
        return msg

    def recipients(self):
        return self.to + self.cc + self.bcc


class EmailMultiAlternatives(mail.EmailMessage):
    multipart_subtype = "alternative"

    def attach_alternative(self, content, mimetype=None):
        self.attach(content=content, mimetype=mimetype)
