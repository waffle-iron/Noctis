from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class nStatusType(models.Model):
    """
    All statuses have to have a type. This is there identifier. The
    components themselves can become more modular in the long run.
    
    @param::name: The name of the status type
    @type::name: CharField
    """
    name = models.CharField(max_length=150)

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

class nStatusComponent(models.Model):
    """
    When the project comes into form. You'll want a simple method for
    determining both the minutia status for individual components as
    well as broad themed access to information between pieces/projects.

    @param::status_type: The type od the status to be used
    @type::status_type: ForeignKey(nStatusType)
    """
    status_type = models.ForeignKey(nStatusType, on_delete=models.CASCADE)
    status_level = models.ForeignKey(nStatusComponentLevel, on_delete=models.CASCADE)
