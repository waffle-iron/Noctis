"""
Simple additional models taken from across the web.
- PrettyTrue
"""

import ast
import json
from django.db import models

## For reference. The JSON field retricts us to postgres but has
## so much potential for dynamic, badass db calling.
# from django.contrib.postgres.fields import JSONField

## TODO: Is there a clean way to add a JSONfield for other
## db types without getting into the habbit of adding app after app?

class ListField(models.TextField):
    """
    Also yanked from the internet. Simple List -> Str -> List
    for storing data.
    """

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)