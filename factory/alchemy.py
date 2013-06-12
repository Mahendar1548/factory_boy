# -*- coding: utf-8 -*-
# Copyright (c) 2013 Romain Commandé
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

from . import base

try:
    from sqlalchemy.sql.functions import max
except ImportError:
    def max():
        raise ImportError('sqlalchemy is not found!')


class SQLAlchemyModelFactory(base.Factory):
    """Factory for SQLAlchemy models. """

    ABSTRACT_FACTORY = True

    @classmethod
    def _setup_next_sequence(cls, *args, **kwargs):
        """Compute the next available PK, based on the 'pk' database field."""
        session = cls.FACTORY_SESSION
        pk = cls.FACTORY_FOR.__table__.primary_key.columns.values()[0].key
        max_pk = session.query(max(getattr(cls.FACTORY_FOR, pk))).one()
        if isinstance(max_pk[0], int):
            return max_pk[0] + 1 if max_pk[0] else 1
        else:
            return 1

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        session = cls.FACTORY_SESSION
        obj = target_class(*args, **kwargs)
        session.add(obj)
        return obj
