from django.db import models
from django.utils.encoding import python_2_unicode_compatible

## Other Apps
from nTracking.models import nStatusComponent

class nProjectType(models.Model):
    """
    If your pipeline supports multiple different project types
    (i.e: film, process, vfx, etc.) you can specify which type
    it falls under to help organize elements/give permissions
    more easily.

    @param::name: The name of the project type
    @type::name: CharField
    """

    name = models.CharField(max_length=150)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProjectPartType(models.Model):
    """
    Even the parts have a type no? Managing this should be simple
    enough.

    @param::name: The name of the project part type
    @type::name: CharField
    """

    name = models.CharField(max_length=150)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProject(models.Model):
    """
    The base object for a project. (Obviously)
    This is more of a concept than a concreet usable item for now.
    With the idea of this repo being open there can be any number
    of way to apply this object.

    Think of it more as a container while the other apps start to
    refine the use and specificity. Nothing should become too strict.
    Modularity is always key.

    @param::name: The name of the project
    @type::name: CharField

    @param::short: The short name of the project. Cleanliness
    @type::short: CharField
    """

    name = models.CharField(max_length=150)
    short = models.CharField(max_length=10, default="")

    project_type = models.ForeignKey(nProjectType, null=True, on_delete=models.CASCADE)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProjectHub(models.Model):
    """
    If the nProject in the pizza this is the crust holding each
    project part together. Designed as a potentailly transparent
    or optional argument, the Hub can be the shot while the ProjectPart
    can be the sub-process assigned to it.

    @param::part_type: The type of part this is (ehh..)
    @type::part_type: nProjectPartType
    """

    ## Because these may link together we can pool the same ProjectPartTypes
    part_type = models.ForeignKey(nProjectPartType, null=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProjectPart(models.Model):
    """
    If the nProject is the pizza, this is the slice. Using parts
    of a project can be thought of as:
    shots->film
    departments->vfx workflow

    Whatever direction you take with this, consider the iplimentaion
    vs. output you'll get from organizing it into the overall data
    structure.

    @param::part_type: The type of part this is (ehh..)
    @type::part_type: nProjectPartType
    """
    
    ## What kind of project part are we working on?
    part_type = models.ForeignKey(nProjectPartType, null=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    ## When it comes down to it we'll need each component to have
    ## tracking markers. How we decide to handle that can vary on
    ## the project/pipeline. Hence why tracking is it's own app.
    track_status = models.ForeignKey(nStatusComponent, null=True, on_delete=models.CASCADE)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name