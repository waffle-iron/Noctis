'''
:PrettyTrue:
This is built to quickly add data to a new/renewed setup that allows
for multiple levels of testing. Adding to this slowly as models/views
take shape with be helpful. I recomend adding simple additions here.
'''

## TODO :: Keep populating this with a simple setup. Make it hefty.
## i.e. -> Something thousands of times to really stress performance
## early on.

## Communication with database
from jsonrpc.proxy import ServiceProxy
S = ServiceProxy("http://localhost:9878/json/")


## Assets

## This, in my opinion, is the most sound layout/general rule of
## thumb-ish to follow when setting up your pathing structures.
## /mnt/server/projects/project_name/project_hub_group_name/ \
##      project_hub/project_part/asset_type/asset_identity/version/asset
## It's quite long and intense but gives us all of the information we
## might need if data is lost. Noctis's GENERATE commands can also let
## us push data to files for reconstruction down the road.

## I've mounted a samba drive (to keep it interesting) called valles.
## Your setup might be different.
dirs = ["/mnt/valles/projects/noc/tst/tst_0101/3d/project_files/tst_0101_test_project/0001/tst_0101_test_project.ma",
        "/mnt/valles/projects/noc/tst/tst_0101/3d/renders/main_layers/0001/tst_0101_test_project/tst_0101_main_layers_0001.%08d.exr"]


## Approvals
init_approval_levels = ["In House", "QC", "Client"]
for a_level in init_approval_levels:
    res = S.nTracking.add_approval_level(a_level)
    if res:
        print "%s added to database..."%a_level 
    else:
        print "%s not added to database..."%a_level 
        
