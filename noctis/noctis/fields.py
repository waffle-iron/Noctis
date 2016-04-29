"""
Simple additional models taken from across the web.
- PrettyTrue
"""

import ast
import json
import settings
from django.db import models

## For reference. The JSON field restricts us to postgres but has
## so much potential for dynamic, bad-ass db calling.
# from django.contrib.postgres.fields import JSONField

## TODO: Is there a clean way to add a JSONfield for other
## db types without getting into the habit of adding app after app?

class PathField(models.TextField):
    '''
    A custom field to handle the pathing structures presented in Noctis
    and the surrounding ecosystem. This will hopefully one day lean on
    Machine Learning to populate and comprehend pathing structures.
    '''

    __metaclass__ = models.SubfieldBase

    def __init(self, *args, **kwargs):
        super(PathField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = {}

        if isinstance(value, dict):
            return value

        _field_return = {}
        for a_field in value.split(settings.PATH_SPLIT):
            pass ## TODO

class ListField(models.TextField):
    '''
    Yanked from the Internet. Simple List -> Str -> List
    for storing data.
    '''

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