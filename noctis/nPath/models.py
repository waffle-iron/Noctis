from django.db import models
from django.utils.encoding import python_2_unicode_compatible

## Other Apps
from nProject.models import nProject

class nPath(models.Model):
    """
    The base object for handling pathing in the Noctis environment.

    @param::name: Name of the nPath structure.
    @type::name: CharField

    @param::path_setup: The syntax of the current structure being used.
    @type::path_setup: TextField

    @param::project: The nProject this nPath is assigned to. If none is given
    then the 'nWORLD' is assigned
    @type::project: ForeignKey(nProject)
    """

    name = models.CharField(max_length=200)
    path_setup = models.TextField()
    project = models.ForeignKey(nProject, on_delete=models.CASCADE)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

    ## Manipulating path_setup ##