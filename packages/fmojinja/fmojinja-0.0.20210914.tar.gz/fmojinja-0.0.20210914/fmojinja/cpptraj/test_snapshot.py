from unittest import TestCase
from fmojinja.cpptraj.snapshot import Snapshot
from fmojinja.__version__ import get_version
from pathlib import Path


class TestSnapshot(TestCase):
    test = Snapshot()

    def test_simple_1(self):
        """
        simple test 1 for snapshot
        python -m fmojinja.cpptraj snapshot -p test.prm -y test.crd --align-mask :1-100 --mask !:NA,WAT,HOH\
        --prefix snapshots/
        :return: None
        """
        lines = self.test.render(
            anchor="@CA,C,N",
            mask="!:NA,WAT,HOH",
            align_mask=":1-100",
            trajin=[Path("test.crd")],
            parm=Path("test.prm"),
            prefix="snapshots/",
        ).splitlines()
        self.assertEqual(lines[0], f"# Generated by fmojinja version {get_version()}")
        self.assertEqual(lines[3], "autoimage anchor @CA,C,N origin", "autoimage with anchor")
        self.assertEqual(lines[4], "align :1-100 move !:NA,WAT,HOH first", "align with anchor with moving mask")
        self.assertEqual(lines[6], "reference test.crd lastframe", "strip")
        self.assertEqual(lines[7], "strip !(!:NA,WAT,HOH)", "strip with mask")
        self.assertEqual(lines[8], "parmwrite out snapshots/test.parm", "write parameters")
        self.assertEqual(lines[9], "outtraj snapshots/test.pdb trajout onlyframes 1 nobox pdbter topresnum", "write pdb")
        self.assertEqual(lines[10], "trajout snapshots/test.rst onlyframes 1", "write rst files")
        self.assertEqual(lines[11], "unstrip", "need to unstrip.")
        self.assertEqual(lines[13], "run")

    def test_simple_2(self):
        """
        simple test 2 for snapshot
        python -m fmojinja.cpptraj snapshot -p test.prm -y test1.crd test2.crd --align-mask :1-100 --mask !:NA,WAT,HOH\
        --prefix snapshots/ -ref ref.crd
        :return: None
        """
        lines = self.test.render(
            anchor="@CA,C,N",
            mask="!:NA,WAT,HOH",
            align_mask=":1-100",
            trajin=[Path("test1.crd"), Path("test2.crd")],
            parm=Path("test.prm"),
            prefix="snapshots/",
            ref=Path("ref.crd")
        ).splitlines()
        self.assertEqual(lines[0], f"# Generated by fmojinja version {get_version()}")
        self.assertEqual(lines[2], "trajin test1.crd lastframe", "")
        self.assertEqual(lines[3], "trajin test2.crd lastframe", "")
        self.assertEqual(lines[4], "autoimage anchor @CA,C,N origin", "autoimage with anchor")
        self.assertEqual(lines[5], "align :1-100 move !:NA,WAT,HOH ref ref.crd", "align with anchor with moving mask with ref")
        self.assertEqual(lines[7], "reference test1.crd lastframe", "strip")
        self.assertEqual(lines[14], "strip !(!:NA,WAT,HOH)", "strip with mask")
        self.assertEqual(lines[15], "parmwrite out snapshots/test2.parm", "write parameters")
        self.assertEqual(lines[16], "outtraj snapshots/test2.pdb trajout onlyframes 2 nobox pdbter topresnum", "write pdb")
        self.assertEqual(lines[17], "trajout snapshots/test2.rst onlyframes 2", "write rst files")
        self.assertEqual(lines[18], "unstrip", "need to unstrip.")
        self.assertEqual(lines[20], "run")


