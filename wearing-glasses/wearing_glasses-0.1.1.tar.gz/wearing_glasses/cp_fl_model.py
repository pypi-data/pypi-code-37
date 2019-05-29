# -*- coding: utf-8 -*-
# Generate images for Face API example running
# BIG CHENG, init 2019/03/25
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


from __future__ import print_function
import click
import os
#import shutil

@click.command()
#@click.argument('path2download', default=".")

def main():

    ## copy images
    cmd = "wget https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2?raw=true -O shape_predictor_68_face_landmarks.dat.bz2"
    #os.system(cmd)
    cmd = "bunzip2 shape_predictor_68_face_landmarks.dat.bz2"
    os.system(cmd)


if __name__ == "__main__":
    main()



