from django.db import models
from django.utils.encoding import python_2_unicode_compatible

## Other Models:

## Extra Fields:
from noctis.fields import ListField

## History Tracking
from simple_history.models import HistoricalRecords

## Utilitis
from noctis.utils import clean_query

## python:
from datetime import datetime

'''
Approvals.
Working with a pointer setup. Testing this will be important
to keep everything in sync but will free up table-space and give central point
of access to managed tracking data.

Another import note is benefits to removing approval from direct contact with
other models. An approval can simultaneously point to multiple parts and link
elements that have no real connection. Keeping this on a clean, sustainable
level of abstraction will help.

NOTE:
Tracking should not be imported by any other models. This is a top level concept.
'''

class nApprovalLevel(models.Model):
    """
    Where the real tracking starts. The most basic level
    of approval markers. These will need to be preprocessed.
    """
    name = models.CharField(max_length=64, unique=True)

### ABSTRACT ###
class nAbstractApproval(models.Model):
    """
    Approvals can range from both single perspective to
    a broad angled one covering multiple pieces.
    """
    approval_level = models.ForeignKey(nApprovalLevel, on_delete=models.CASCADE)
    achieved_on = models.DateTimeField(default=datetime.now(), auto_now=False)

    ## In noctis we use the concept of organic(0) - stale(1) - ripe(2) data.
    ## meaning there is room to conditionally organize and manage
    ## large sets of objects based on whether or not we can trust
    ## the information.
    age = models.IntegerField(default=0)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nMainApproval(nAbstractApproval):
    """
    The approval can take many forms but we'll try
    to keep it abstract as possible while getting the idea
    across to the user/developer.
    """

    ## Avoid cyclic dependency
    from nAsset.models import nAsset
    from nProject.models import nProject, nProjectHub, nProjectPart

    ## All can be null to allow for dynamic 'linking' of objects.
    project_pointer = models.ForeignKey(nProject, null=True, on_delete=models.CASCADE)
    hub_pointer = models.ForeignKey(nProjectHub, null=True, on_delete=models.CASCADE)
    part_pointer = models.ForeignKey(nProjectPart, null=True, on_delete=models.CASCADE)
    asset_pointer = models.ForeignKey(nAsset, on_delete=models.CASCADE)

    def __repr__(self):
        return "<Asset Approval, %d > %s>"%(self.id, self.asset.id)

    @classmethod
    def dict_fields(cls):
        fields = [f.name for f in cls._meta.fields]
        fields.extend("project_pointer__name",
                      "hub_pointer__name",
                      "part_pointer__name",
                      "asset_pointer__asset_type",
                      "asset_pointer__version",
                      "asset_pointer__version_controller__group_name")
        return fields

    @classmethod
    def make_dicts(cls, query_on, fields=[]):
        if not fields:
            fields = cls.dict_fields()
        values = list(query_on.values(*fields))

        return_values = []
        for an_approval in values:
            return_values.append(clean_query(values))

        return return_values