# -*- coding: utf-8 -*-
# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Tests that HTML generation is awesome."""

import datetime
import glob
import json
import os
import os.path
import re
import sys

import coverage
from coverage.backward import unicode_class
from coverage import env
from coverage.files import flat_rootname
import coverage.html
from coverage.misc import CoverageException, NotPython, NoSource

from tests.coveragetest import CoverageTest, TESTS_DIR
from tests.goldtest import gold_path
from tests.goldtest import change_dir, compare, contains, doesnt_contain, contains_any


class HtmlTestHelpers(CoverageTest):
    """Methods that help with HTML tests."""

    def create_initial_files(self):
        """Create the source files we need to run these tests."""
        self.make_file("main_file.py", """\
            import helper1, helper2
            helper1.func1(12)
            helper2.func2(12)
            """)
        self.make_file("helper1.py", """\
            def func1(x):
                if x % 2:
                    print("odd")
            """)
        self.make_file("helper2.py", """\
            def func2(x):
                print("x is %d" % x)
            """)

    def run_coverage(self, covargs=None, htmlargs=None):
        """Run coverage.py on main_file.py, and create an HTML report."""
        self.clean_local_file_imports()
        cov = coverage.Coverage(**(covargs or {}))
        self.start_import_stop(cov, "main_file")
        return cov.html_report(**(htmlargs or {}))

    def remove_html_files(self):
        """Remove the HTML files created as part of the HTML report."""
        os.remove("htmlcov/index.html")
        os.remove("htmlcov/main_file_py.html")
        os.remove("htmlcov/helper1_py.html")
        os.remove("htmlcov/helper2_py.html")

    def get_html_report_content(self, module):
        """Return the content of the HTML report for `module`."""
        filename = module.replace(".", "_").replace("/", "_") + ".html"
        filename = os.path.join("htmlcov", filename)
        with open(filename) as f:
            return f.read()

    def get_html_index_content(self):
        """Return the content of index.html.

        Timestamps are replaced with a placeholder so that clocks don't matter.

        """
        with open("htmlcov/index.html") as f:
            index = f.read()
        index = re.sub(
            r"created at \d{4}-\d{2}-\d{2} \d{2}:\d{2}",
            r"created at YYYY-MM-DD HH:MM",
            index,
        )
        return index

    def assert_correct_timestamp(self, html):
        """Extract the timestamp from `html`, and assert it is recent."""
        timestamp_pat = r"created at (\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})"
        m = re.search(timestamp_pat, html)
        self.assertTrue(m, "Didn't find a timestamp!")
        timestamp = datetime.datetime(*map(int, m.groups()))
        # The timestamp only records the minute, so the delta could be from
        # 12:00 to 12:01:59, or two minutes.
        self.assert_recent_datetime(
            timestamp,
            seconds=120,
            msg="Timestamp is wrong: {0}".format(timestamp),
        )


class HtmlDeltaTest(HtmlTestHelpers, CoverageTest):
    """Tests of the HTML delta speed-ups."""

    def setUp(self):
        super(HtmlDeltaTest, self).setUp()

        # At least one of our tests monkey-patches the version of coverage.py,
        # so grab it here to restore it later.
        self.real_coverage_version = coverage.__version__
        self.addCleanup(setattr, coverage, "__version__", self.real_coverage_version)

    def run_coverage(self, covargs=None, htmlargs=None):
        """For the delta tests, we always want source=. """
        covargs = covargs or {}
        covargs['source'] = "."
        super(HtmlDeltaTest, self).run_coverage(covargs=covargs, htmlargs=htmlargs)

    def test_html_created(self):
        # Test basic HTML generation: files should be created.
        self.create_initial_files()
        self.run_coverage()

        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/main_file_py.html")
        self.assert_exists("htmlcov/helper1_py.html")
        self.assert_exists("htmlcov/helper2_py.html")
        self.assert_exists("htmlcov/style.css")
        self.assert_exists("htmlcov/coverage_html.js")

    def test_html_delta_from_source_change(self):
        # HTML generation can create only the files that have changed.
        # In this case, helper1 changes because its source is different.
        self.create_initial_files()
        self.run_coverage()
        index1 = self.get_html_index_content()
        self.remove_html_files()

        # Now change a file and do it again
        self.make_file("helper1.py", """\
            def func1(x):   # A nice function
                if x % 2:
                    print("odd")
            """)

        self.run_coverage()

        # Only the changed files should have been created.
        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/helper1_py.html")
        self.assert_doesnt_exist("htmlcov/main_file_py.html")
        self.assert_doesnt_exist("htmlcov/helper2_py.html")
        index2 = self.get_html_index_content()
        self.assertMultiLineEqual(index1, index2)

    def test_html_delta_from_coverage_change(self):
        # HTML generation can create only the files that have changed.
        # In this case, helper1 changes because its coverage is different.
        self.create_initial_files()
        self.run_coverage()
        self.remove_html_files()

        # Now change a file and do it again
        self.make_file("main_file.py", """\
            import helper1, helper2
            helper1.func1(23)
            helper2.func2(23)
            """)

        self.run_coverage()

        # Only the changed files should have been created.
        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/helper1_py.html")
        self.assert_exists("htmlcov/main_file_py.html")
        self.assert_doesnt_exist("htmlcov/helper2_py.html")

    def test_html_delta_from_settings_change(self):
        # HTML generation can create only the files that have changed.
        # In this case, everything changes because the coverage.py settings
        # have changed.
        self.create_initial_files()
        self.run_coverage(covargs=dict(omit=[]))
        index1 = self.get_html_index_content()
        self.remove_html_files()

        self.run_coverage(covargs=dict(omit=['xyzzy*']))

        # All the files have been reported again.
        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/helper1_py.html")
        self.assert_exists("htmlcov/main_file_py.html")
        self.assert_exists("htmlcov/helper2_py.html")
        index2 = self.get_html_index_content()
        self.assertMultiLineEqual(index1, index2)

    def test_html_delta_from_coverage_version_change(self):
        # HTML generation can create only the files that have changed.
        # In this case, everything changes because the coverage.py version has
        # changed.
        self.create_initial_files()
        self.run_coverage()
        index1 = self.get_html_index_content()
        self.remove_html_files()

        # "Upgrade" coverage.py!
        coverage.__version__ = "XYZZY"

        self.run_coverage()

        # All the files have been reported again.
        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/helper1_py.html")
        self.assert_exists("htmlcov/main_file_py.html")
        self.assert_exists("htmlcov/helper2_py.html")
        index2 = self.get_html_index_content()
        fixed_index2 = index2.replace("XYZZY", self.real_coverage_version)
        self.assertMultiLineEqual(index1, fixed_index2)

    def test_file_becomes_100(self):
        self.create_initial_files()
        self.run_coverage()

        # Now change a file and do it again
        self.make_file("main_file.py", """\
            import helper1, helper2
            # helper1 is now 100%
            helper1.func1(12)
            helper1.func1(23)
            """)

        self.run_coverage(htmlargs=dict(skip_covered=True))

        # The 100% file, skipped, shouldn't be here.
        self.assert_doesnt_exist("htmlcov/helper1_py.html")

    def test_status_format_change(self):
        self.create_initial_files()
        self.run_coverage()
        self.remove_html_files()

        with open("htmlcov/status.json") as status_json:
            status_data = json.load(status_json)

        self.assertEqual(status_data['format'], 1)
        status_data['format'] = 2
        with open("htmlcov/status.json", "w") as status_json:
            json.dump(status_data, status_json)

        self.run_coverage()

        # All the files have been reported again.
        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/helper1_py.html")
        self.assert_exists("htmlcov/main_file_py.html")
        self.assert_exists("htmlcov/helper2_py.html")


class HtmlTitleTest(HtmlTestHelpers, CoverageTest):
    """Tests of the HTML title support."""

    def test_default_title(self):
        self.create_initial_files()
        self.run_coverage()
        index = self.get_html_index_content()
        self.assertIn("<title>Coverage report</title>", index)
        self.assertIn("<h1>Coverage report:", index)

    def test_title_set_in_config_file(self):
        self.create_initial_files()
        self.make_file(".coveragerc", "[html]\ntitle = Metrics & stuff!\n")
        self.run_coverage()
        index = self.get_html_index_content()
        self.assertIn("<title>Metrics &amp; stuff!</title>", index)
        self.assertIn("<h1>Metrics &amp; stuff!:", index)

    def test_non_ascii_title_set_in_config_file(self):
        self.create_initial_files()
        self.make_file(".coveragerc", "[html]\ntitle = «ταБЬℓσ» numbers")
        self.run_coverage()
        index = self.get_html_index_content()
        self.assertIn(
            "<title>&#171;&#964;&#945;&#1041;&#1068;&#8467;&#963;&#187;"
            " numbers", index
        )
        self.assertIn(
            "<h1>&#171;&#964;&#945;&#1041;&#1068;&#8467;&#963;&#187;"
            " numbers", index
        )

    def test_title_set_in_args(self):
        self.create_initial_files()
        self.make_file(".coveragerc", "[html]\ntitle = Good title\n")
        self.run_coverage(htmlargs=dict(title="«ταБЬℓσ» & stüff!"))
        index = self.get_html_index_content()
        self.assertIn(
            "<title>&#171;&#964;&#945;&#1041;&#1068;&#8467;&#963;&#187;"
            " &amp; st&#252;ff!</title>", index
        )
        self.assertIn(
            "<h1>&#171;&#964;&#945;&#1041;&#1068;&#8467;&#963;&#187;"
            " &amp; st&#252;ff!:", index
        )


class HtmlWithUnparsableFilesTest(HtmlTestHelpers, CoverageTest):
    """Test the behavior when measuring unparsable files."""

    def test_dotpy_not_python(self):
        self.make_file("main.py", "import innocuous")
        self.make_file("innocuous.py", "a = 1")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "main")
        self.make_file("innocuous.py", "<h1>This isn't python!</h1>")
        msg = "Couldn't parse '.*innocuous.py' as Python source: .* at line 1"
        with self.assertRaisesRegex(NotPython, msg):
            cov.html_report()

    def test_dotpy_not_python_ignored(self):
        self.make_file("main.py", "import innocuous")
        self.make_file("innocuous.py", "a = 2")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "main")
        self.make_file("innocuous.py", "<h1>This isn't python!</h1>")
        cov.html_report(ignore_errors=True)
        self.assertEqual(
            len(cov._warnings),
            1,
            "Expected a warning to be thrown when an invalid python file is parsed")
        self.assertIn(
            "Could not parse Python file",
            cov._warnings[0],
            "Warning message should be in 'invalid file' warning"
        )
        self.assertIn(
            "innocuous.py",
            cov._warnings[0],
            "Filename should be in 'invalid file' warning"
        )
        self.assert_exists("htmlcov/index.html")
        # This would be better as a glob, if the HTML layout changes:
        self.assert_doesnt_exist("htmlcov/innocuous.html")

    def test_dothtml_not_python(self):
        # We run a .html file, and when reporting, we can't parse it as
        # Python.  Since it wasn't .py, no error is reported.

        # Run an "HTML" file
        self.make_file("innocuous.html", "a = 3")
        self.run_command("coverage run --source=. innocuous.html")
        # Before reporting, change it to be an HTML file.
        self.make_file("innocuous.html", "<h1>This isn't python at all!</h1>")
        output = self.run_command("coverage html")
        self.assertEqual(output.strip(), "No data to report.")

    def test_execed_liar_ignored(self):
        # Jinja2 sets __file__ to be a non-Python file, and then execs code.
        # If that file contains non-Python code, a TokenError shouldn't
        # have been raised when writing the HTML report.
        source = "exec(compile('','','exec'), {'__file__': 'liar.html'})"
        self.make_file("liar.py", source)
        self.make_file("liar.html", "{# Whoops, not python code #}")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "liar")
        cov.html_report()
        self.assert_exists("htmlcov/index.html")

    def test_execed_liar_ignored_indentation_error(self):
        # Jinja2 sets __file__ to be a non-Python file, and then execs code.
        # If that file contains untokenizable code, we shouldn't get an
        # exception.
        source = "exec(compile('','','exec'), {'__file__': 'liar.html'})"
        self.make_file("liar.py", source)
        # Tokenize will raise an IndentationError if it can't dedent.
        self.make_file("liar.html", "0\n  2\n 1\n")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "liar")
        cov.html_report()
        self.assert_exists("htmlcov/index.html")

    def test_decode_error(self):
        # https://bitbucket.org/ned/coveragepy/issue/351/files-with-incorrect-encoding-are-ignored
        # imp.load_module won't load a file with an undecodable character
        # in a comment, though Python will run them.  So we'll change the
        # file after running.
        self.make_file("main.py", "import sub.not_ascii")
        self.make_file("sub/__init__.py")
        self.make_file("sub/not_ascii.py", """\
            # coding: utf-8
            a = 1  # Isn't this great?!
            """)
        cov = coverage.Coverage()
        self.start_import_stop(cov, "main")

        # Create the undecodable version of the file. make_file is too helpful,
        # so get down and dirty with bytes.
        with open("sub/not_ascii.py", "wb") as f:
            f.write(b"# coding: utf-8\na = 1  # Isn't this great?\xcb!\n")

        with open("sub/not_ascii.py", "rb") as f:
            undecodable = f.read()
        self.assertIn(b"?\xcb!", undecodable)

        cov.html_report()

        html_report = self.get_html_report_content("sub/not_ascii.py")
        expected = "# Isn't this great?&#65533;!"
        self.assertIn(expected, html_report)

    def test_formfeeds(self):
        # https://bitbucket.org/ned/coveragepy/issue/360/html-reports-get-confused-by-l-in-the-code
        self.make_file("formfeed.py", "line_one = 1\n\f\nline_two = 2\n")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "formfeed")
        cov.html_report()

        formfeed_html = self.get_html_report_content("formfeed.py")
        self.assertIn("line_two", formfeed_html)


class HtmlTest(HtmlTestHelpers, CoverageTest):
    """Moar HTML tests."""

    def test_missing_source_file_incorrect_message(self):
        # https://bitbucket.org/ned/coveragepy/issue/60
        self.make_file("thefile.py", "import sub.another\n")
        self.make_file("sub/__init__.py", "")
        self.make_file("sub/another.py", "print('another')\n")
        cov = coverage.Coverage()
        self.start_import_stop(cov, 'thefile')
        os.remove("sub/another.py")

        missing_file = os.path.join(self.temp_dir, "sub", "another.py")
        missing_file = os.path.realpath(missing_file)
        msg = "(?i)No source for code: '%s'" % re.escape(missing_file)
        with self.assertRaisesRegex(NoSource, msg):
            cov.html_report()

    def test_extensionless_file_collides_with_extension(self):
        # It used to be that "program" and "program.py" would both be reported
        # to "program.html".  Now they are not.
        # https://bitbucket.org/ned/coveragepy/issue/69
        self.make_file("program", "import program\n")
        self.make_file("program.py", "a = 1\n")
        self.run_command("coverage run program")
        self.run_command("coverage html")
        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/program.html")
        self.assert_exists("htmlcov/program_py.html")

    def test_has_date_stamp_in_files(self):
        self.create_initial_files()
        self.run_coverage()

        with open("htmlcov/index.html") as f:
            self.assert_correct_timestamp(f.read())
        with open("htmlcov/main_file_py.html") as f:
            self.assert_correct_timestamp(f.read())

    def test_reporting_on_unmeasured_file(self):
        # It should be ok to ask for an HTML report on a file that wasn't even
        # measured at all.  https://bitbucket.org/ned/coveragepy/issues/403
        self.create_initial_files()
        self.make_file("other.py", "a = 1\n")
        self.run_coverage(htmlargs=dict(morfs=['other.py']))
        self.assert_exists("htmlcov/index.html")
        self.assert_exists("htmlcov/other_py.html")

    def test_shining_panda_fix(self):
        # The ShiningPanda plugin looks for "status.dat" to find HTML reports.
        # Accommodate them, but only if we are running under Jenkins.
        self.set_environ("JENKINS_URL", "Something or other")
        self.create_initial_files()
        self.run_coverage()
        self.assert_exists("htmlcov/status.dat")

    def test_report_skip_covered_no_branches(self):
        self.make_file("main_file.py", """
            import not_covered

            def normal():
                print("z")
            normal()
        """)
        self.make_file("not_covered.py", """
            def not_covered():
                print("n")
        """)
        self.run_coverage(htmlargs=dict(skip_covered=True))
        self.assert_exists("htmlcov/index.html")
        self.assert_doesnt_exist("htmlcov/main_file_py.html")
        self.assert_exists("htmlcov/not_covered_py.html")

    def test_report_skip_covered_100(self):
        self.make_file("main_file.py", """
            def normal():
                print("z")
            normal()
        """)
        res = self.run_coverage(covargs=dict(source="."), htmlargs=dict(skip_covered=True))
        self.assertEqual(res, 100.0)
        self.assert_doesnt_exist("htmlcov/main_file_py.html")

    def test_report_skip_covered_branches(self):
        self.make_file("main_file.py", """
            import not_covered

            def normal():
                print("z")
            normal()
        """)
        self.make_file("not_covered.py", """
            def not_covered():
                print("n")
        """)
        self.run_coverage(covargs=dict(branch=True), htmlargs=dict(skip_covered=True))
        self.assert_exists("htmlcov/index.html")
        self.assert_doesnt_exist("htmlcov/main_file_py.html")
        self.assert_exists("htmlcov/not_covered_py.html")


class HtmlStaticFileTest(CoverageTest):
    """Tests of the static file copying for the HTML report."""

    def setUp(self):
        super(HtmlStaticFileTest, self).setUp()
        original_path = list(coverage.html.STATIC_PATH)
        self.addCleanup(setattr, coverage.html, 'STATIC_PATH', original_path)

    def test_copying_static_files_from_system(self):
        # Make a new place for static files.
        self.make_file("static_here/jquery.min.js", "Not Really JQuery!")
        coverage.html.STATIC_PATH.insert(0, "static_here")

        self.make_file("main.py", "print(17)")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "main")
        cov.html_report()

        with open("htmlcov/jquery.min.js") as f:
            jquery = f.read()
        self.assertEqual(jquery, "Not Really JQuery!")

    def test_copying_static_files_from_system_in_dir(self):
        # Make a new place for static files.
        INSTALLED = [
            "jquery/jquery.min.js",
            "jquery-hotkeys/jquery.hotkeys.js",
            "jquery-isonscreen/jquery.isonscreen.js",
            "jquery-tablesorter/jquery.tablesorter.min.js",
        ]
        for fpath in INSTALLED:
            self.make_file(os.path.join("static_here", fpath), "Not real.")
        coverage.html.STATIC_PATH.insert(0, "static_here")

        self.make_file("main.py", "print(17)")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "main")
        cov.html_report()

        for fpath in INSTALLED:
            the_file = os.path.basename(fpath)
            with open(os.path.join("htmlcov", the_file)) as f:
                contents = f.read()
            self.assertEqual(contents, "Not real.")

    def test_cant_find_static_files(self):
        # Make the path point to useless places.
        coverage.html.STATIC_PATH = ["/xyzzy"]

        self.make_file("main.py", "print(17)")
        cov = coverage.Coverage()
        self.start_import_stop(cov, "main")
        msg = "Couldn't find static file u?'.*'"
        with self.assertRaisesRegex(CoverageException, msg):
            cov.html_report()

def filepath_to_regex(path):
    """Create a regex for scrubbing a file path."""
    regex = re.escape(path)
    # If there's a backslash, let it match either slash.
    regex = regex.replace(r"\\", r"[\\/]")
    if env.WINDOWS:
        regex = "(?i)" + regex
    return regex


def compare_html(expected, actual):
    """Specialized compare function for our HTML files."""
    scrubs = [
        (r'/coverage.readthedocs.io/?[-.\w/]*', '/coverage.readthedocs.io/VER'),
        (r'coverage.py v[\d.abc]+', 'coverage.py vVER'),
        (r'created at \d\d\d\d-\d\d-\d\d \d\d:\d\d', 'created at DATE'),
        # Some words are identifiers in one version, keywords in another.
        (r'<span class="(nam|key)">(print|True|False)</span>', r'<span class="nam">\2</span>'),
        # Occasionally an absolute path is in the HTML report.
        (filepath_to_regex(TESTS_DIR), 'TESTS_DIR'),
        (r'/Users/ned/coverage/trunk/tests', 'TESTS_DIR'),
        (filepath_to_regex(flat_rootname(unicode_class(TESTS_DIR))), '_TESTS_DIR'),
        (flat_rootname(u'/Users/ned/coverage/trunk/tests'), '_TESTS_DIR'),
        # The temp dir the tests make.
        (filepath_to_regex(os.getcwd()), 'TEST_TMPDIR'),
        (filepath_to_regex(flat_rootname(unicode_class(os.getcwd()))), '_TEST_TMPDIR'),
        (r'/private/var/folders/[\w/]{35}/coverage_test/tests_test_html_\w+_\d{8}', 'TEST_TMPDIR'),
        (r'_private_var_folders_\w{35}_coverage_test_tests_test_html_\w+_\d{8}', '_TEST_TMPDIR'),
    ]
    if env.WINDOWS:
        # For file paths...
        scrubs += [(r"\\", "/")]
    compare(expected, actual, file_pattern="*.html", scrubs=scrubs)


class HtmlGoldTests(CoverageTest):
    """Tests of HTML reporting that use gold files."""

    def test_a(self):
        self.make_file("a.py", """\
            if 1 < 2:
                # Needed a < to look at HTML entities.
                a = 3
            else:
                a = 4
            """)

        cov = coverage.Coverage()
        a = self.start_import_stop(cov, "a")
        cov.html_report(a, directory='out')

        compare_html(gold_path("html/a"), "out")
        contains(
            "out/a_py.html",
            ('<span class="key">if</span> <span class="num">1</span> '
             '<span class="op">&lt;</span> <span class="num">2</span>'),
            ('    <span class="nam">a</span> '
             '<span class="op">=</span> <span class="num">3</span>'),
            '<span class="pc_cov">67%</span>',
        )
        contains(
            "out/index.html",
            '<a href="a_py.html">a.py</a>',
            '<span class="pc_cov">67%</span>',
            '<td class="right" data-ratio="2 3">67%</td>',
        )

    def test_b_branch(self):
        self.make_file("b.py", """\
            def one(x):
                # This will be a branch that misses the else.
                if x < 2:
                    a = 3
                else:
                    a = 4

            one(1)

            def two(x):
                # A missed else that branches to "exit"
                if x:
                    a = 5

            two(1)

            def three():
                try:
                    # This if has two branches, *neither* one taken.
                    if name_error_this_variable_doesnt_exist:
                        a = 1
                    else:
                        a = 2
                except:
                    pass

            three()
            """)

        cov = coverage.Coverage(branch=True)
        b = self.start_import_stop(cov, "b")
        cov.html_report(b, directory="out")

        compare_html(gold_path("html/b_branch"), "out")
        contains(
            "out/b_py.html",
            ('<span class="key">if</span> <span class="nam">x</span> '
             '<span class="op">&lt;</span> <span class="num">2</span>'),
            ('    <span class="nam">a</span> <span class="op">=</span> '
             '<span class="num">3</span>'),
            '<span class="pc_cov">70%</span>',

            ('<span class="annotate short">3&#x202F;&#x219B;&#x202F;6</span>'
             '<span class="annotate long">line 3 didn\'t jump to line 6, '
                            'because the condition on line 3 was never false</span>'),
            ('<span class="annotate short">12&#x202F;&#x219B;&#x202F;exit</span>'
             '<span class="annotate long">line 12 didn\'t return from function \'two\', '
                            'because the condition on line 12 was never false</span>'),
            ('<span class="annotate short">20&#x202F;&#x219B;&#x202F;21,&nbsp;&nbsp; '
                            '20&#x202F;&#x219B;&#x202F;23</span>'
             '<span class="annotate long">2 missed branches: '
                            '1) line 20 didn\'t jump to line 21, '
                                'because the condition on line 20 was never true, '
                            '2) line 20 didn\'t jump to line 23, '
                                'because the condition on line 20 was never false</span>'),
        )
        contains(
            "out/index.html",
            '<a href="b_py.html">b.py</a>',
            '<span class="pc_cov">70%</span>',
            '<td class="right" data-ratio="16 23">70%</td>',
        )

    def test_bom(self):
        self.make_file("bom.py", bytes=b"""\
\xef\xbb\xbf# A Python source file in utf-8, with BOM.
math = "3\xc3\x974 = 12, \xc3\xb72 = 6\xc2\xb10"

import sys

if sys.version_info >= (3, 0):
    assert len(math) == 18
    assert len(math.encode('utf-8')) == 21
else:
    assert len(math) == 21
    assert len(math.decode('utf-8')) == 18
""".replace(b"\n", b"\r\n"))

        # It's important that the source file really have a BOM, which can
        # get lost, so check that it's really there, and that we have \r\n
        # line endings.
        with open("bom.py", "rb") as f:
            data = f.read()
            assert data[:3] == b"\xef\xbb\xbf"
            assert data.count(b"\r\n") == 11

        cov = coverage.Coverage()
        bom = self.start_import_stop(cov, "bom")
        cov.html_report(bom, directory="out")

        compare_html(gold_path("html/bom"), "out")
        contains(
            "out/bom_py.html",
            '<span class="str">"3&#215;4 = 12, &#247;2 = 6&#177;0"</span>',
        )

    def test_isolatin1(self):
        self.make_file("isolatin1.py", bytes=b"""\
# -*- coding: iso8859-1 -*-
# A Python source file in another encoding.

math = "3\xd74 = 12, \xf72 = 6\xb10"
assert len(math) == 18
""")

        cov = coverage.Coverage()
        isolatin1 = self.start_import_stop(cov, "isolatin1")
        cov.html_report(isolatin1, directory="out")

        compare_html(gold_path("html/isolatin1"), "out")
        contains(
            "out/isolatin1_py.html",
            '<span class="str">"3&#215;4 = 12, &#247;2 = 6&#177;0"</span>',
        )

    def make_main_etc(self):
        """Make main.py and m1-m3.py for other tests."""
        self.make_file("main.py", """\
            import m1
            import m2
            import m3

            a = 5
            b = 6

            assert m1.m1a == 1
            assert m2.m2a == 1
            assert m3.m3a == 1
            """)
        self.make_file("m1.py", """\
            m1a = 1
            m1b = 2
            """)
        self.make_file("m2.py", """\
            m2a = 1
            m2b = 2
            """)
        self.make_file("m3.py", """\
            m3a = 1
            m3b = 2
            """)

    def test_omit_1(self):
        self.make_main_etc()
        cov = coverage.Coverage(include=["./*"])
        self.start_import_stop(cov, "main")
        cov.html_report(directory="out")
        compare_html(gold_path("html/omit_1"), "out")

    def test_omit_2(self):
        self.make_main_etc()
        cov = coverage.Coverage(include=["./*"])
        self.start_import_stop(cov, "main")
        cov.html_report(directory="out", omit=["m1.py"])
        compare_html(gold_path("html/omit_2"), "out")

    def test_omit_3(self):
        self.make_main_etc()
        cov = coverage.Coverage(include=["./*"])
        self.start_import_stop(cov, "main")
        cov.html_report(directory="out", omit=["m1.py", "m2.py"])
        compare_html(gold_path("html/omit_3"), "out")

    def test_omit_4(self):
        self.make_main_etc()
        self.make_file("omit4.ini", """\
            [report]
            omit = m2.py
            """)

        cov = coverage.Coverage(config_file="omit4.ini", include=["./*"])
        self.start_import_stop(cov, "main")
        cov.html_report(directory="out")
        compare_html(gold_path("html/omit_4"), "out")

    def test_omit_5(self):
        self.make_main_etc()
        self.make_file("omit5.ini", """\
            [report]
            omit =
                fooey
                gooey, m[23]*, kablooey
                helloworld

            [html]
            directory = out/omit_5
            """)

        cov = coverage.Coverage(config_file="omit5.ini", include=["./*"])
        self.start_import_stop(cov, "main")
        cov.html_report()
        compare_html(gold_path("html/omit_5"), "out/omit_5")

    def test_other(self):
        self.make_file("src/here.py", """\
            import other

            if 1 < 2:
                h = 3
            else:
                h = 4
            """)
        self.make_file("othersrc/other.py", """\
            # A file in another directory.  We're checking that it ends up in the
            # HTML report.

            print("This is the other src!")
            """)

        with change_dir("src"):
            sys.path.insert(0, "")          # pytest sometimes has this, sometimes not!?
            sys.path.insert(0, "../othersrc")
            cov = coverage.Coverage(include=["./*", "../othersrc/*"])
            self.start_import_stop(cov, "here")
            cov.html_report(directory="../out")

        # Different platforms will name the "other" file differently. Rename it
        for p in glob.glob("out/*_other_py.html"):
            os.rename(p, "out/blah_blah_other_py.html")

        compare_html(gold_path("html/other"), "out")
        contains(
            "out/index.html",
            '<a href="here_py.html">here.py</a>',
            'other_py.html">', 'other.py</a>',
        )

    def test_partial(self):
        self.make_file("partial.py", """\
            # partial branches and excluded lines
            a = 6

            while "no peephole".upper():        # t4
                break

            while a:        # pragma: no branch
                break

            if 0:
                never_happen()

            if 1:
                a = 21

            if a == 23:
                raise AssertionError("Can't")
            """)
        self.make_file("partial.ini", """\
            [run]
            branch = True

            [report]
            exclude_lines =
                raise AssertionError
            """)

        cov = coverage.Coverage(config_file="partial.ini")
        partial = self.start_import_stop(cov, "partial")
        cov.html_report(partial, directory="out")

        compare_html(gold_path("html/partial"), "out")
        contains(
            "out/partial_py.html",
            '<p id="t4" class="stm par run hide_run">',
            '<p id="t7" class="stm run hide_run">',
            # The "if 0" and "if 1" statements are optimized away.
            '<p id="t10" class="pln">',
            # The "raise AssertionError" is excluded by regex in the .ini.
            '<p id="t17" class="exc">',
        )
        contains(
            "out/index.html",
            '<a href="partial_py.html">partial.py</a>',
        )
        contains(
            "out/index.html",
            '<span class="pc_cov">91%</span>'
        )

    def test_styled(self):
        self.make_file("a.py", """\
            if 1 < 2:
                # Needed a < to look at HTML entities.
                a = 3
            else:
                a = 4
            """)

        self.make_file("extra.css", "/* Doesn't matter what goes in here, it gets copied. */\n")

        cov = coverage.Coverage()
        a = self.start_import_stop(cov, "a")
        cov.html_report(a, directory="out", extra_css="extra.css")

        compare_html(gold_path("html/styled"), "out")
        compare(gold_path("html/styled"), "out", file_pattern="*.css")
        contains(
            "out/a_py.html",
            '<link rel="stylesheet" href="extra.css" type="text/css">',
            ('<span class="key">if</span> <span class="num">1</span> '
             '<span class="op">&lt;</span> <span class="num">2</span>'),
            ('    <span class="nam">a</span> <span class="op">=</span> '
             '<span class="num">3</span>'),
            '<span class="pc_cov">67%</span>'
        )
        contains(
            "out/index.html",
            '<link rel="stylesheet" href="extra.css" type="text/css">',
            '<a href="a_py.html">a.py</a>',
            '<span class="pc_cov">67%</span>'
        )

    def test_tabbed(self):
        # The file contents would look like this with 8-space tabs:
        #   x = 1
        #   if x:
        #           a = "tabbed"                            # aligned comments
        #           if x:                                   # look nice
        #                   b = "no spaces"                 # when they
        #           c = "done"                              # line up.
        self.make_file("tabbed.py", """\
            x = 1
            if x:
            \ta = "Tabbed"\t\t\t\t# Aligned comments
            \tif x:\t\t\t\t\t# look nice
            \t\tb = "No spaces"\t\t\t# when they
            \tc = "Done"\t\t\t\t# line up.
            """)

        cov = coverage.Coverage()
        tabbed = self.start_import_stop(cov, "tabbed")
        cov.html_report(tabbed, directory="out")

        # Editors like to change things, make sure our source file still has tabs.
        contains("tabbed.py", "\tif x:\t\t\t\t\t# look nice")

        contains(
            "out/tabbed_py.html",
            '>        <span class="key">if</span> '
            '<span class="nam">x</span><span class="op">:</span>'
            '                                   '
            '<span class="com"># look nice</span>'
        )

        doesnt_contain("out/tabbed_py.html", "\t")

    def test_unicode(self):
        self.make_file("unicode.py", """\
            # -*- coding: utf-8 -*-
            # A Python source file with exotic characters.

            upside_down = "ʎd˙ǝbɐɹǝʌoɔ"
            surrogate = "db40,dd00: x󠄀"
            """)

        cov = coverage.Coverage()
        unimod = self.start_import_stop(cov, "unicode")
        cov.html_report(unimod, directory="out")

        compare_html(gold_path("html/unicode"), "out")
        contains(
            "out/unicode_py.html",
            '<span class="str">"&#654;d&#729;&#477;b&#592;&#633;&#477;&#652;o&#596;"</span>',
        )

        contains_any(
            "out/unicode_py.html",
            '<span class="str">"db40,dd00: x&#56128;&#56576;"</span>',
            '<span class="str">"db40,dd00: x&#917760;"</span>',
        )
