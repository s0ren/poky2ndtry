import json
import os
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, get_bb_vars

class CVECheck(OESelftestTestCase):

    def test_version_compare(self):
        from oe.cve_check import Version

        result = Version("100") > Version("99")
        self.assertTrue( result, msg="Failed to compare version '100' > '99'")
        result = Version("2.3.1") > Version("2.2.3")
        self.assertTrue( result, msg="Failed to compare version '2.3.1' > '2.2.3'")
        result = Version("2021-01-21") > Version("2020-12-25")
        self.assertTrue( result, msg="Failed to compare version '2021-01-21' > '2020-12-25'")
        result = Version("1.2-20200910") < Version("1.2-20200920")
        self.assertTrue( result, msg="Failed to compare version '1.2-20200910' < '1.2-20200920'")

        result = Version("1.0") >= Version("1.0beta")
        self.assertTrue( result, msg="Failed to compare version '1.0' >= '1.0beta'")
        result = Version("1.0-rc2") > Version("1.0-rc1")
        self.assertTrue( result, msg="Failed to compare version '1.0-rc2' > '1.0-rc1'")
        result = Version("1.0.alpha1") < Version("1.0")
        self.assertTrue( result, msg="Failed to compare version '1.0.alpha1' < '1.0'")
        result = Version("1.0_dev") <= Version("1.0")
        self.assertTrue( result, msg="Failed to compare version '1.0_dev' <= '1.0'")

        # ignore "p1" and "p2", so these should be equal
        result = Version("1.0p2") == Version("1.0p1")
        self.assertTrue( result ,msg="Failed to compare version '1.0p2' to '1.0p1'")
        # ignore the "b" and "r"
        result = Version("1.0b") == Version("1.0r")
        self.assertTrue( result ,msg="Failed to compare version '1.0b' to '1.0r'")

        # consider the trailing alphabet as patched level when comparing
        result = Version("1.0b","alphabetical") < Version("1.0r","alphabetical")
        self.assertTrue( result ,msg="Failed to compare version with suffix '1.0b' < '1.0r'")
        result = Version("1.0b","alphabetical") > Version("1.0","alphabetical")
        self.assertTrue( result ,msg="Failed to compare version with suffix '1.0b' > '1.0'")

        # consider the trailing "p" and "patch" as patched released when comparing
        result = Version("1.0","patch") < Version("1.0p1","patch")
        self.assertTrue( result ,msg="Failed to compare version with suffix '1.0' < '1.0p1'")
        result = Version("1.0p2","patch") > Version("1.0p1","patch")
        self.assertTrue( result ,msg="Failed to compare version with suffix '1.0p2' > '1.0p1'")
        result = Version("1.0_patch2","patch") < Version("1.0_patch3","patch")
        self.assertTrue( result ,msg="Failed to compare version with suffix '1.0_patch2' < '1.0_patch3'")


    def test_recipe_report_json(self):
        config = """
INHERIT += "cve-check"
CVE_CHECK_FORMAT_JSON = "1"
"""
        self.write_config(config)

        vars = get_bb_vars(["CVE_CHECK_SUMMARY_DIR", "CVE_CHECK_SUMMARY_FILE_NAME_JSON"])
        summary_json = os.path.join(vars["CVE_CHECK_SUMMARY_DIR"], vars["CVE_CHECK_SUMMARY_FILE_NAME_JSON"])
        recipe_json = os.path.join(vars["CVE_CHECK_SUMMARY_DIR"], "m4-native_cve.json")

        try:
            os.remove(summary_json)
            os.remove(recipe_json)
        except FileNotFoundError:
            pass

        bitbake("m4-native -c cve_check")

        def check_m4_json(filename):
            with open(filename) as f:
                report = json.load(f)
            self.assertEqual(report["version"], "1")
            self.assertEqual(len(report["package"]), 1)
            package = report["package"][0]
            self.assertEqual(package["name"], "m4-native")
            found_cves = { issue["id"]: issue["status"] for issue in package["issue"]}
            self.assertIn("CVE-2008-1687", found_cves)
            self.assertEqual(found_cves["CVE-2008-1687"], "Patched")

        self.assertExists(summary_json)
        check_m4_json(summary_json)
        self.assertExists(recipe_json)
        check_m4_json(recipe_json)


    def test_image_json(self):
        config = """
INHERIT += "cve-check"
CVE_CHECK_FORMAT_JSON = "1"
"""
        self.write_config(config)

        vars = get_bb_vars(["CVE_CHECK_DIR", "CVE_CHECK_SUMMARY_DIR", "CVE_CHECK_SUMMARY_FILE_NAME_JSON"])
        report_json = os.path.join(vars["CVE_CHECK_SUMMARY_DIR"], vars["CVE_CHECK_SUMMARY_FILE_NAME_JSON"])
        print(report_json)
        try:
            os.remove(report_json)
        except FileNotFoundError:
            pass

        bitbake("core-image-minimal-initramfs")
        self.assertExists(report_json)

        # Check that the summary report lists at least one package
        with open(report_json) as f:
            report = json.load(f)
        self.assertEqual(report["version"], "1")
        self.assertGreater(len(report["package"]), 1)

        # Check that a random recipe wrote a recipe report to deploy/cve/
        recipename = report["package"][0]["name"]
        recipe_report = os.path.join(vars["CVE_CHECK_DIR"], recipename + "_cve.json")
        self.assertExists(recipe_report)
        with open(recipe_report) as f:
            report = json.load(f)
        self.assertEqual(report["version"], "1")
        self.assertEqual(len(report["package"]), 1)
        self.assertEqual(report["package"][0]["name"], recipename)
