#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `create` package."""


import unittest
from click.testing import CliRunner

from create import create
from create import cli


class TestCreate(unittest.TestCase):
    """Tests for `create` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
    def tearDown(self):
        """Tear down test fixtures, if any."""
        assert 2==2
    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        #assert result.exit_code == 0
        #assert 'create.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
