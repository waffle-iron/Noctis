from django.shortcuts import render
from jsonrpc import jsonrpc_method

## Other models:
from nPath.models import nPath

## Models:
from .models import nAsset
from .models import nAssetType
from .models import nVersionControler

## Other Python:
from noctis import utils

@jsonrpc_method("nAsset.create_asset(str, str, int, str, str, str, int) -> dict")
def create_asset(request, asset_pointer="", asset_type="", version=0,
                 version_controler="", path_setup=""):
    """
    Create an nAsset. This takes quite a few params but needs to be potent and
    well connected. This has to point quite a few directions without being dependant
    on too much.

    path_setup example :
        setup_name -'Noctis_Maya_Project'
        setup_style - /@share@/@server@/projects/@project@/...

    """
    _u = utils.getUsername(request)
    _a_type = nAssetType.objects.get(name=asset_type)

    ## Pathing break down to give us any other information we'll
    ## need. This gives us fine tuned control as long as the path
    ## minimums are kept in the setup.
    _path_data = nPath.breakdown(path_setup, asset_pointer)

    ## Getting the version controller requires nowing the project name
    _version_control = nVersionControler.objects.get()

    asset = nAsset.objects.create(asset_pointer=asset_pointer,
                                  asset_type=_a_type,
                                  version=version,
                                  version_controler=)
