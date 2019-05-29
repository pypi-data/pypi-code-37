# -*- coding: utf-8 -*-
# Wearing Glasses helper
# BIG CHENG, init 2019/05/29
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

msg_cp_fl_model = "cp_fl_model [dir_for_running]"
msg_plot_glasses = "plot_glasses [dir_for_input_image dir_for_output_image]"
msgs = [msg_cp_fl_model, msg_plot_glasses]


@click.command()
def main():

    print("plot glasses commands:")
    for msg in msgs:
        print("\t"+msg)
    

if __name__ == "__main__":
    main()
