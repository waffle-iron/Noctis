from django.test import TestCase

from nProject.models import nProject
from nProject.models import nProjectType
from nProject.models import nProjectPartType
from nProject.models import nProjectHub

from nAsset.models import nAssetType
from nAsset.models import nAsset
from nAsset.models import nVersionController

class AssetTestCase(TestCase):

    def setUp(self):
        self.test_file = "//cortex/projects/tbt/the_whole_test/%s.txt"
        at = nAssetType.objects.create(name="t_type")
        pType = nProjectType.objects.create(name="vfx")
        ppType = nProjectPartType.objects.create(name="DoBigThings")
        prj = nProject.objects.create(name="The Big Test",
                                      short="tbt",
                                       project_type=pType)
        nProjectHub.objects.create(part_type=ppType,
                                   name="tb0001",
                                   project=prj)

    def test_create_asset_manual(self):
        _group_name = "test"
        pHub = nProjectHub.objects.get(name="tb0001")
        prj = nProject.objects.get(short="tbt")
        at = nAssetType.objects.get(name="t_type")
        vc = nVersionController.objects.create(highest_version=1,
                                               group_name=_group_name,
                                               hub_pointer=pHub,
                                               asset_type=at)

        ace = nAsset.objects.create(asset_pointer=self.test_file%("file1"),
                                    version=1,
                                    version_controller=vc,
                                    author="prettytrue")

        self.assertEqual(ace.version, 1)
        # self.assertEqual(ace.author, "notme")

    def test_create_asset_rpc(self):
        from nAsset.views import create_asset
        prj = nProject.objects.get(short="tbt")
        res = create_asset(None,
                           asset_pointer=self.test_file%("file2"),
                           asset_type="t_type",
                           version=1,
                           asset_name="a_file",
                           hub_name="tb0001",
                           project_name=prj.name)

        self.assertEqual(res['version'], 1)
