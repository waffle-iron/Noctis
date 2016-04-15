from django.shortcuts import render
from jsonrpc import jsonrpc_method

## Other models:
from nPath.models import nPath
from nPath.views import extract_basic
from nProject.models import nProjectPart
from nProject.models import nProjectHub

## Models:
from .models import nAsset
from .models import nAssetType
from .models import nVersionController

## Other/Misc:
from noctis import utils

@jsonrpc_method("nAsset.create_asset(str, str, int, str, str, str, int) -> dict")
def create_asset(request, asset_pointer="", asset_type="", version=0,
                 asset_name="", hub_name="", project_name=""):
    """
    Create an nAsset. This takes quite a few params but needs to be potent and
    well connected. This has to point quite a few directions without being dependent
    on too much.

    path_setup example :
        setup_name -'Noctis_Maya_Project'
        setup_style - /@share@/@server@/projects/@project@/...

    @params
    $asset_pointer : (str) : give us the path we;re working with.

    $asset_type : (str) : What kind of asset is this?

    $version : (int) : The version of the asset we're going to add

    $asset_name : (str) : Name to be tied to the asset for Version Group control

    $hub_name : (str) : The name associated with this 
    """
    if request:
        _u = utils.getUsername(request)
    else:
        _u = "aimee"
    _a_type = nAssetType.objects.get(name=asset_type)

    ## Pathing break down to give us any other information we'll
    ## need. This gives us fine tuned control as long as the path
    ## minimums are kept in the setup.
    _path_data = extract_basic(asset_pointer)
    if not _path_data:
        e = "The path: %s isn't compatible with Nocits."%asset_pointer
        e += "(There must be an extension)"
        raise TypeError(e)
    # path_setup = nPath.objects.get(extension=_path_data['ext'], asset_type=asset_type)
    hub = nProjectHub.objects.get(name=hub_name, project__name=project_name)

    ## Getting the version controller requires knowing the project name
    version_control, created = nVersionController.objects.get_or_create(hub_pointer=hub,
                                                                       group_name=asset_name,
                                                                       asset_type=_a_type)

    if version_control.highest_version < version:
        version_control.highest_version = version
        version_control.save() # To keep our new data

    asset = nAsset.objects.create(asset_pointer=asset_pointer,
                                  version=version,
                                  version_controller=version_control,
                                  project_hub=hub,
                                  author=_u)

    return {}
