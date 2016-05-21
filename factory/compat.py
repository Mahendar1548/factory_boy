# -*- coding: utf-8 -*-
# Copyright (c) 2010 Mark Sandstrom
# Copyright (c) 2011-2015 Raphaël Barrois
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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Compatibility tools"""

import datetime
import decimal
import sys

PY2 = (sys.version_info[0] == 2)

if PY2:  # pragma: no cover
    def is_string(obj):
        return isinstance(obj, (str, unicode))

    from StringIO import StringIO as BytesIO

    def force_text(str_or_unicode):
        if isinstance(str_or_unicode, unicode):
            return str_or_unicode
        return str_or_unicode.decode('utf-8')

else:  # pragma: no cover
    def is_string(obj):
        return isinstance(obj, str)

    from io import BytesIO

    def force_text(text):
        return text


try:  # pragma: no cover
    # Python >= 3.2
    UTC = datetime.timezone.utc
except AttributeError:  # pragma: no cover
    try:
        # Fallback to pytz
        from pytz import UTC
    except ImportError:

        # Ok, let's write our own.
        class _UTC(datetime.tzinfo):
            """The UTC tzinfo."""

            def utcoffset(self, dt):
                return datetime.timedelta(0)

            def tzname(self, dt):
                return "UTC"

            def dst(self, dt):
                return datetime.timedelta(0)

            def localize(self, dt):
                dt.astimezone(self)

        UTC = _UTC()
