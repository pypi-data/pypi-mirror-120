#  Copyright 2020 IBM Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re as regex

from typing import List, Optional

import click

import dg.config
import dg.config.cluster_credentials_manager
import dg.lib.click.utils
import dg.lib.fyre.cluster
import dg.utils.network

from dg.lib.fyre.ocp_plus_api_manager import OCPPlusAPIManager
from dg.lib.fyre.utils.click import fyre_command_options
from dg.utils.logging import loglevel_command


def validate_node_name(ctx, param, value) -> Optional[str]:
    if value is not None and regex.match("worker\\d+$", value) is None:
        raise click.BadParameter("Invalid worker node name")

    return value


@loglevel_command(
    context_settings=dg.lib.click.utils.create_default_map_from_dict(
        dg.config.cluster_credentials_manager.cluster_credentials_manager.get_current_credentials()
    )
)
@fyre_command_options
@click.option("--additional-disk-size", help="Size of additional disk", multiple=True, type=click.IntRange(1, 1000))
@click.option("--cluster-name", help="Name of the OCP+ cluster to be edited", required=True)
@click.option("--force", "-f", help="Skip confirmation", is_flag=True)
@click.option("--node-name", callback=validate_node_name, help="Node name", required=True)
@click.option("--node-num-cpus", help="Number of CPUs per node", type=click.IntRange(1, 16))
@click.option("--node-ram-size", help="RAM size per node", type=click.IntRange(1, 64))
@click.option("--site", help="OCP+ site", type=click.Choice(["rtp", "svl"]))
def edit_worker_node(
    fyre_api_user_name: str,
    fyre_api_key: str,
    additional_disk_size: List[int],
    cluster_name: str,
    force: bool,
    node_name: str,
    node_num_cpus: Optional[int],
    node_ram_size: Optional[int],
    site: Optional[str],
):
    """Edit a worker node of an OCP+ cluster"""

    if (len(additional_disk_size) != 0) or (node_num_cpus is not None) or (node_ram_size is not None):
        if not force:
            click.confirm(f"Do you really want to edit node '{node_name}' of cluster '{cluster_name}'?", abort=True)

        dg.utils.network.disable_insecure_request_warning()
        OCPPlusAPIManager(fyre_api_user_name, fyre_api_key).edit_worker_node(
            cluster_name, node_name, additional_disk_size, node_num_cpus, node_ram_size, site
        )
