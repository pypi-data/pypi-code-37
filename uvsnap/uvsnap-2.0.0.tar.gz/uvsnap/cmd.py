#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""UVSnap Commands."""

import argparse
import os
import tempfile

import uvsnap

__author__ = 'Greg Albrecht <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def cli():
    """Command Line interface for UVSnap."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-n', '--nvr_url', help='NVR URL'
    )
    parser.add_argument(
        '-a', '--api_key', help='NVR API Key'
    )
    parser.add_argument(
        '-d', '--directory', help='Snapshot Directory',
        default=tempfile.mkdtemp()
    )
    parser.add_argument(
        '-V', '--verbose', help='Verbose Output', action='store_true'
    )
    parser.add_argument(
        'command', metavar='CMD', type=str,
        help='One of: "all", "list" or CAMERA_ID'
    )

    opts = parser.parse_args()

    nvr = uvsnap.NVR(opts.nvr_url, opts.api_key)
    nvr.get_cameras()

    if opts.command == 'list':
        cam_list = []
        for camera in nvr.cameras:
            state = 'UNKNOWN'
            if 'DISCONNECTED' in camera['state']:
                state = 'OFFLINE'
            elif 'CONNECTED' in camera['state']:
                state = 'online'
            _msg = '{:<26}||{:^10}|| {:<30}'.format(
                camera['_id'], state, camera['name'])
            cam_list.append(_msg)

        print("\n".join(cam_list))

    elif opts.command == 'all':
        if not os.path.exists(opts.directory):
            os.makedirs(opts.directory)

        snapshots = nvr.get_all_snapshots()

        for camera_id, snapshot in snapshots.items():
            if snapshot is not None:
                output_file = os.path.join(
                    opts.directory, '%s.jpg' % camera_id)

                with open(output_file, 'wb') as ofd:
                    ofd.write(snapshot)

                if opts.verbose:
                    print('Wrote Snapshot: {}'.format(output_file))

    elif opts.command == 'get_snapshot_url':
        if not nvr.cameras:
            nvr.get_cameras()

        for camera in nvr.cameras:
            print(nvr.get_snapshot_url(camera))
    else:
        camera_id = None
        for camera in nvr.cameras:
            if opts.command in camera['_id']:
                camera_id = camera['_id']

        if camera_id is None:
            print('Camera {} not found.'.format(opts.command))

        if not os.path.exists(opts.directory):
            os.makedirs(opts.directory)

        snapshot = nvr.get_snapshot(camera_id)

        if snapshot is not None:
            output_file = os.path.join(opts.directory, '%s.jpg' % camera_id)

            with open(output_file, 'w') as ofd:
                ofd.write(snapshot)

            if opts.verbose:
                print('Wrote Snapshot: {}'.format(output_file))
