from django.db import models
from django.core.exceptions import ValidationError

## Extra fields
from noctis.fields import ListField

## Defaults:
from nTracking.defaults.tracking_defaults import default_status_breakdown_config

## Python
from datetime import datetime

'''
Status Work. Areas dealing with overall progress of nProjectParts/Hubs.
'''

def status_breakdown_test(config):
    if isinstance(config, list):
        for aStatus in config:
            status_match = nStatusComponentLevel.objects.filter(name=aStatus)
            if status_match.exists():
                e =  ("ERROR: %s not found in database. Add it as a \
                Component Level or remove it form the list."%aStatus)
                raise ValidationError(e)
        return True
    raise ValidationError("ERROR: config is not a list type.")

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