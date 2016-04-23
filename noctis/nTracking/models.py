from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

## Other Models:

## Extra Fields:
from noctis.fields import ListField

## Defaults:
from nTracking.defaults.tracking_defaults import default_status_breakdown_config

## History Tracking
from simple_history.models import HistoricalRecords

## python:
from datetime import datetime

'''
Status Work. Areas dealing with overall progress of nProjectParts/Hubs
'''

def status_breakdown_test(config):
    if isinstance(config, list):
        for aStatus in config:
            status_match = nStatusComponentLevel.objects.get(name=aStatus)
            print ("ERROR: %s not found in database. Add it as a \
            Component Level or remove it form the list."%aStatus)
            if not status_match:
                raise ValidationError
        return True
    print ("ERROR: config is not a list type.")
    raise ValidationError

class nStatusType(models.Model):
    """
    All statuses have to have a type. This is there identifier. The
    components themselves can become more modular in the long run.
    
    @param::name: The name of the status type
    @type::name: CharField

    @param::status_breakdown: The actual breakdown that a status
    goes through as it passes markers.
    @type::status_breakdown: ListField
    @i.e.: ["name_of_SCL1", "name_of_SCL2", ...]
    """
    name = models.CharField(max_length=150, unique=True)
    status_breakdown = ListField(default=default_status_breakdown_config,
                                 validators=[status_breakdown_test])

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nStatusComponentLevel(models.Model):
    """
    The component status should have to have markers
    as it walks through the pipeline(s). This is that marker.
    """
    name = models.CharField(max_length=150, unique=True)
    value = models.IntegerField(default=0)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nStatusComponent(models.Model):
    """
    When the project comes into form. You'll want a simple method for
    determining both the minutia status for individual components as
    well as broad themed access to information between pieces/projects.

    @param::status_type: The type of the status to be used
    @type::status_type: ForeignKey(nStatusType)

    @param::status_level: The completion amount given the set Status Type
    @type::status_level: ForeignKey(nStatusComponentLevel)
    """
    status_type = models.ForeignKey(nStatusType, on_delete=models.CASCADE)
    status_level = models.ForeignKey(nStatusComponentLevel, on_delete=models.CASCADE)

    ## Tracking history here will be important
    history = HistoricalRecords()

    ## For fast return of the status level
    @python_2_unicode_compatible
    def __str__(self):
        return self.status_level.name

    def percentComplete(self):
        return (float(self.status_level.value)/float(self.status_type.total_status_components))*100.0

    def getHistory(self):
        raise NotImplementedError # TODO


'''
Approvals. Working with a pointer setup. Testing this will be important
to keep everything in sync but will free up table-space and give central point
of access to managed tracking data.

Another import note is benefits to removing approval from direct contact with
other models. An approval can simultaneously point to multiple parts and link
elements that have no real connection. Keeping this on a clean, sustainable
level of abstraction will help 
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
    achieved_on = models.DateTimeField(default=datetime.now, auto_now=False)

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
    def to_dict(cls, query_on):
        fields = cls.dict_fields()
        values = list(query_on.values(*fields))
        return values
