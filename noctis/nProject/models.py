from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class nProject(models.Model):
    """
    The base object for a project. (Obviously)
    This is more of a concept than a concert, usable item for now.
    With the idea of this repo being open there can be any number
    of way to apply this object.

    Think of it more as a container while the other apps start to
    refine the use and specificity. Nothing should become too strict.
    Modularity is always key.

    When things aren't in some way linked to a particular nProject they
    should always default to the nWORLD nProject to keep things consistant.

    nWORLD is useful for multiple reasons. (!$! Fill in why...)

    @param::name: The name of the project
    @type::name: CharField
    """

    name = models.CharField(max_length=200)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name
