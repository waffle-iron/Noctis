from django.db import models
from django.utils.encoding import python_2_unicode_compatible

## Other Apps
from nPath.models import nPath
from nProject.models import nProjectPart
from nProject.models import nProjectHub

## Utilitis
from noctis.utils import organize_values

class nAssetType(models.Model):
    """
    What are we actually using when it comes to the nAsset
    """
    
    name = models.CharField(max_length=150, default="")

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

class nVersionController(models.Model):
    """
    In order to most effectively collate objects into the same
    space we need a method of organizing them and placing them into
    sequential buckets. This allows us to do just that.

    @param::highest_version: The current highest version available
    for that group of assets.
    @type::highest_version: Int 
    """

    highest_version = models.IntegerField(default=1)

    ## To keep assets in an even more organized fashion we can add a
    ## parameter to track multiple of the same object_type without
    ## version matching
    group_name = models.CharField(max_length=64, default="")

    ## This is the pointer that lets us keep unique identification
    ## down to a certain level.
    hub_pointer = models.ForeignKey(nProjectHub, null=True, on_delete=models.CASCADE)

    ## Here's where we'll house the type of our assets. This is because
    ## a group should contain only one type of asset!
    asset_type = models.ForeignKey(nAssetType, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hub_pointer', 'group_name', 'asset_type')

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
    The main model for any form of singular object component management
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
    
    ## This mainly points to a path. While it has the ability to act as more than
    ## that it will take a little massaging in other models/views.
    asset_pointer = models.CharField(max_length=300, default="")

    ## For a good basic relationship between iterations we're going to let
    ## version control/asset 'typing' be dealt with inter-asset-wise
    version = models.IntegerField(default=0)
    version_controller = models.ForeignKey(nVersionController, null=True, on_delete=models.SET_NULL)

    ## For digital assets we may want to link a hard file path
    ## with nPath giving the ability to extract/understand information
    ## from it
    # path_setup = models.ForeignKey(nPath, null=True, on_delete=models.SET_NULL)

    ## Organization ## -> Pushed to the Version Controller
    # project_hub = models.ForeignKey(nProjectHub, null=True, on_delete=models.CASCADE)

    ## Another piece of assets comes in the perspective of scope.
    ## When we're looking at something like assets it can be hard
    ## to obtain singular information from certain distances
    ## In order to fix this we can rely on the approval system in
    ## the nTracking model.
    ## These are established in a 'pointer' fashion to avoid overloading
    ## this table as much as possible. Lean and mean is the goal.

    ## Information handles.
    author = models.CharField(max_length=64, default="")

    ### Methods ###
    @python_2_unicode_compatible
    def __str__(self):
        return self.name

    @python_2_unicode_compatible
    def getGroupName(self):
        return version_controller.group_name

    @classmethod
    def make_dicts(cls, q):
        ## To make a dictionary out of the objects at maximum performance
        ## let's lean on the database rather than Python.
        asset_fields = [field.name for field in cls._meta.fields]
        version_controller_list =  [ "version_controller__group_name",
                                     "version_controller__asset_type__name",
                                     "version_controller__hub_pointer" ]
        asset_fields.extend(version_controller_list)
        asset_values = list(q.values(*asset_fields))

        ## Organize our tables.
        vn = 'version_controller'
        # asset_results = []
        for an_asset in asset_values:
            # asset_results.append(organize_values([vn], an_asset))
            version_controller_table = {}
            vc_id = an_asset[vn]
            an_asset[vn] = dict(id=vc_id)
            for a_vc_value in version_controller_list:
                an_asset[vn][a_vc_value[len(vn)+2:]] = an_asset.pop(a_vc_value)
            an_asset[vn]['asset_type'] = { 'name' : an_asset[vn].pop('asset_type__name') }

        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(asset_values)
        return asset_values
