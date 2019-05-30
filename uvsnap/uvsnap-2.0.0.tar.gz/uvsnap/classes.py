#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""UVSnap Module Class Definitions."""

import json
import logging
import logging.handlers

import requests

import uvsnap

__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


requests.packages.urllib3.disable_warnings()


class NVR(object):

    """NVR Object."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(uvsnap.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(uvsnap.LOG_LEVEL)
        _console_handler.setFormatter(uvsnap.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, nvr_url, api_key):
        self.nvr_url = nvr_url
        self.api_key = api_key

        self.cameras = []

    def get_cameras(self):
        """
        Gets a cameras from the NVR.
        """
        cameras_url = "%s/api/2.0/camera" % self.nvr_url

        get_cameras = requests.get(
            cameras_url,
            params={'apiKey': self.api_key},
            verify=False
        )

        if get_cameras.ok:
            cameras = json.loads(get_cameras.text)
            self.cameras = cameras['data']

    def _get_snapshot(self, camera_id):
        """
        Gets a snapshot for the specified camera from the NVR.

        :param camera_id: NVR Camera ID.
        :type camera_id: str
        :returns: `requests` Object
        """
        if not self.cameras:
            self.get_cameras()

        for camera in self.cameras:
            if camera['state'] == 'CONNECTED' and camera['_id'] == camera_id:
                get_snapshot = requests.get(
                    "%s/api/2.0/snapshot/camera/%s" % (
                        self.nvr_url, camera_id),
                    params={'force': 'true', 'apiKey': self.api_key},
                    verify=False
                )

                if get_snapshot.ok:
                    return get_snapshot

    def get_snapshot(self, camera_id):
        """
        Gets a snapshot for the specified camera ID.

        :param camera_id: NVR Camera ID.
        :type camera_id: str
        :returns: Snapshot data (raw).
        :rtype: str
        """
        snapshot = self._get_snapshot(camera_id)
        if snapshot:
            return snapshot.content

    def get_snapshot_url(self, camera_id):
        """
        Gets a snapshot URL for the specified camera ID.

        :param camera_id: NVR Camera ID.
        :type camera_id: str
        :returns: Snapshot URL.
        :rtype: str
        """
        snapshot = self._get_snapshot(camera_id)
        if snapshot:
            return snapshot.url

    def get_all_snapshots(self):
        """
        Gets a snapshot for all cameras from the NVR.

        :returns: All snapshots.
        """
        snapshots = {}

        if not self.cameras:
            self.get_cameras()

        for camera in self.cameras:
            snapshots[camera['_id']] = self.get_snapshot(camera['_id'])
        return snapshots
