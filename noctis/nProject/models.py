from django.db import models
from django.utils.encoding import python_2_unicode_compatible

## Other Apps
from nStatus.models import nStatusComponent

## Utilitis
from noctis.utils import clean_query

## History Tracking
from simple_history.models import HistoricalRecords

class nProjectType(models.Model):
    """
    If your pipeline supports multiple different project types
    (i.e: film, process, vfx, etc.) you can specify which type
    it falls under to help organize elements/give permissions
    more easily.

    :param::name: The name of the project type
    :type::name: CharField
    """

    name = models.CharField(max_length=150)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProjectPartType(models.Model):
    """
    Even the parts have a type no? Managing this should be simple
    enough.

    :param::name: The name of the project part type
    :type::name: CharField
    """

    name = models.CharField(max_length=150)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProject(models.Model):
    """
    The base object for a project. (Obviously)
    This is more of a concept than a concrete usable item for now.
    With the idea of this repo being open there can be any number
    of way to apply this object.

    Think of it more as a container while the other apps start to
    refine the use and specificity. Nothing should become too strict.
    Modularity is always key.

    :param::name: The name of the project
    :type::name: CharField

    :param::short: The short name of the project. Cleanliness
    :type::short: CharField

    :param::project_type: What type of project are we working with
    :type::project_type: ForeignKey -> nProjectType
    """

    name = models.CharField(max_length=150)
    short = models.CharField(max_length=10, default="")

    project_type = models.ForeignKey(nProjectType, null=True, on_delete=models.CASCADE)

    history = HistoricalRecords()

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProjectHub(models.Model):
    """
    If the nProject in the pizza this is the crust holding each
    project part together. Designed as a potentailly transparent
    or optional argument, the Hub can be the shot while the ProjectPart
    can be the sub-process assigned to it.

    :param::part_type: The type of part this is (ehh..)
    :type::part_type: nProjectPartType

    :param::name: Current name given to this piece
    :type::name: CharField

    :param::project: The nProject this is assigned to.
    :type::project: ForeignKey -> nProject
    """

    ## Because these may link together we can pool the same ProjectPartTypes
    part_type = models.ForeignKey(nProjectPartType, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    project = models.ForeignKey(nProject, null=True, on_delete=models.CASCADE)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nProjectPart(models.Model):
    """
    If the nProject is the pizza, this is the slice. Using parts
    of a project can be thought of as:
    shots->film
    departments->vfx workflow

    Whatever direction you take with this, consider the implementation
    vs. output you'll get from organizing it into the overall data
    structure.

    :param::part_type: The type of part this is (ehh..)
    :type::part_type: nProjectPartType

    :param::name: The name identifier for the part
    :type::name: CharField

    :param::project: The project this part is assigned to.    
    """
    ## Avoid cyclic dependency
    
    ## What kind of project part are we working on?
    part_type = models.ForeignKey(nProjectPartType, null=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    ## When it comes down to it we'll need each component to have
    ## tracking markers. How we decide to handle that can vary on
    ## the project/pipeline. Hence why tracking is it's own app.
    track_status = models.ForeignKey(nStatusComponent, null=True, on_delete=models.CASCADE)

    project = models.ForeignKey(nProject, null=True, on_delete=models.CASCADE)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

    @classmethod
    def dict_fields(cls):
        fields = [field.name for field in cls._meta.fields]
        part_type_fields = ["part_type__name"]
        tracking_fields = ["track_status__status_type__name",
                           "track_status__status_type__id",
                           "track_status__status_type__status_breakdown",
                           "track_status__status_level__name",
                           "track_status__status_level__value"]
        project_field = ["project__short",
                         "project__project_type__name"]

        fields.extend(part_type_fields)
        fields.extend(tracking_fields)
        fields.extend(project_field)

        return fields

    @classmethod
    def make_dicts(cls, q, fields=[]):
        ## To make a dictionary out of the objects at maximum performance
        ## let's lean on the database rather than Python.
        if not fields:
            fields = cls.dict_fields()
        part_values = list(q.values(*fields))

        ## Organie our tables.
        part_results = []
        for a_part in part_values:
            part_results.append(clean_query(a_part))

        return part_results