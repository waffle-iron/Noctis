from django.db import models
from django.utils.encoding import python_2_unicode_compatible

## Other Apps
from nPath.models import nPath
from nProject.models import nProjectPart

class nAssetType(models.Model):
    """
    What are we actually using when it comes to the nAsset
    """
    
    name = models.CharField(max_length=150, default="")

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nVersionControler(models.Model):
    """
    In order to most effectively coalate objects into the same
    space we need a method of organizing them and placing them into
    sequential buckets. This alows us to do just that.

    @param::highest_version: The current highest version available
    for that group of assets.
    @type::highest_version: Int
    """

    highest_version = models.IntegerField(default=0)

    ## To keep assets in an even more organized fashion we can add a
    ## parameter to track multiple of the same object_type without
    ## version matching
    group_name = models.CharField(max_length=300, default="")

    @python_2_unicode_compatible
    def __str__(self):
        return self.group_name

    def versionUp(self, number=1, static=False):
        if static:
            self.highest_version = number
        else:
            self.highest_version += number

class nAsset(models.Model):
    """
    The main object for any form of singular object component management
    in the pipeline. (i.e. a Render, 3D Model, Project File, Scripts, etc.)

    This bad boy has the potential to be both amazing and dangerous.
    When working on this there has to be a strong understanding of
    where the data may be pointing/queried from. For a baseline the
    Asset should rely off of three basic points...
    0=> The Real Object Pointer - The actual location of the data/thing
    1=> The Object Type - What is that object made of
    2=> The Object Relationship(s) - Where does this tie to other elements

    The last of that being the most ambiguous.
    
    Other elements can include things such as pointers to objects that are
    used to handle this asset. Whatever you see fit of course.
    """
    
    # For basic simplicity we'll use a filepath but something
    # else can be used to replace this.
    asset_pointer = models.CharField(max_length=300, default="")
    asset_type = models.ForeignKey(nAssetType, null=True, on_delete=models.SET_NULL)

    ## For a good basic relationship between iterations we're going to let
    ## version control be delt with inter-asset-wise
    version = models.IntegerField(default=0)
    version_controller = models.ForeignKey(nVersionControler, null=True, on_delete=models.SET_NULL)

    ## For digital assets we may want to link a hard file path
    ## with nPath giving the ability to extract/understand information
    ## from it
    path_setup = models.ForeignKey(nPath, null=True, on_delete=models.SET_NULL)

    ## Organization ##
    project_part = models.ForeignKey(nProjectPart, null=True, on_delete=models.CASCADE)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name
