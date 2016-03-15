from django.db import models
from django.utils.encoding import python_2_unicode_compatible

## Extra Fields:
from noctis.fields import ListField

## python
from datetime import datetime

class nStatusType(models.Model):
    """
    All statuses have to have a type. This is there identifier. The
    components themselves can become more modular in the long run.
    
    @param::name: The name of the status type
    @type::name: CharField

    @param::status_breakdown: The actual breakdown that a status
    goes through as it passes markers.
    @type::status_breakdown: ListField
    """
    name = models.CharField(max_length=150)
    total_status_components = models.IntegerField(default=0)
    status_breakdown = ListField(null=True)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nStatusComponentLevel(models.Model):
    """
    The component status should have to have markers
    as it walks through the pipeline(s). This is that marker.
    """
    name = models.CharField(max_length=150)
    value = models.IntegerField(default=0)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nStatusComponentHistory(models.Model):
    """
    Storing history information can be vital in term of keeping
    long stream data organized. Making it acessable can be just
    as vital.
    """

    status_id = models.IntegerField(default=0)
    modified_on = models.DateTimeField(default=datetime.now, auto_now=False)
    status_level = models.ForeignKey(nStatusComponentLevel, on_delete=models.CASCADE)

    @python_2_unicode_compatible
    def __str__(self):
        return "WIP"
        
        ## TODO: sort this better and make it useful... Bad for now.
        _all_inline = nStatusComponentHistory.objects.filter(status_id=self.status_id)
        return str([a.status_level.name for a in _all_inline])


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

    ## For fast return of the status level
    @python_2_unicode_compatible
    def __str__(self):
        return status_level.name

    def percentComplete(self):
        return (float(status_level.value)/float(status_type.total_status_components))*100.0

    def getHistory(self):
        raise NotImplementedError # TODO
