from django.test import TestCase

## This test suite models
from nTracking.models import nMainApproval
from nTracking.models import nApprovalLevel

## Other test models needed
# nAsset
from nAsset.models import nAsset
from nAsset.models import nAssetType
from nAsset.models import nVerisonController
# nProject
from nProject.models import nProject
from nProject.models import nProjectType
from nProject.models import nProjectPartType
from nProject.models import nProjectHub

class TrackingTestCase(TestCase):

    def setUp(self):
        '''
        We're going to set up multiple different test options.
        We'll need an Asset to point.
        '''
        ## Project material setup
        _pt = nProjectType.objects.create(name="tsttype")
        _ppt = nProjectPartType.objects.create(name="DoSmallThings")
        _prj = nProject.objects.create(name="The Small Big",
                                       short="tsb",
                                       project_type=_pt)
        _pjh = nProjectHub.objects.create(part_type=_ppt,
                                          name="tb0001",
                                          project=_prj)

        ## Asset hanlding
        _at = nAssetType.objects.create(name="tstast")
        _vc = nVerisonController.objects.create(highest_version=1,
                                                group_name="test",
                                                hub_pointer=_pjh,
                                                asset_type=_at)
        self.one_asset = nAsset.objects.create(asset_pointer="//cortex/projects/tbt/the_whole_test/file2.txt",
                                               version=1,
                                               version_controller=_vc,
                                               author="prettytrue")

    def test_create_basic_main_approval_to_hub(self):
        '''
        Creating a nMainApproval from Asset <-> Hub
        '''
        _hub = nProjectHub.objects.get(name="tb0001")
        _ma = nMainApproval.objects.create(asset_pointer=self.one_asset,
                                           hub_pointer=_hub)

        self.assertEqual(_ma.asset_pointer.author, "prettytrue")

    def test_create_basic_main_approval_to_part(self):
        '''
        Creating a nMainApproval from nAsset <-> Part
        '''
        ## TOOO..
        pass
