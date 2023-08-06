# Copyright (c) 2019-2020 SAP SE or an SAP affiliate company. All rights reserved. This file is
# licensed under the Apache Software License, v. 2 except as noted otherwise in the LICENSE file
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ensure import ensure_annotations

import functools

import ci.util

from model.concourse import ConcourseConfig, ConcourseUAMConfig, ConcourseUAM, ConcourseTeamConfig
from .api import ConcourseApiFactory

'''
An implementation of the (undocumented [0]) RESTful HTTP API offered by concourse
[1]. It was reverse-engineered based on [2], as well using Chrome developer tools and
POST-Man [3].

Usage:
------

Users will probably want to create an instance of ConcourseApiVX, passing a
ConcourseConfig object to the `from_cfg` factory function.

Other types defined in this module are not intended to be instantiated by users.

[0] https://github.com/concourse/concourse/issues/1122
[1] https://concourse.ci
[2] https://github.com/concourse/concourse/blob/master/atc/routes.go
[3] https://www.getpostman.com/
'''


def lookup_cc_team_cfg(concourse_cfg_name, cfg_set, team_name) -> ConcourseTeamConfig:
    for cc_team_cfg in cfg_set._cfg_elements('concourse_team_cfg'):
        if cc_team_cfg.team_name() != team_name:
            continue
        if concourse_cfg_name != cc_team_cfg.concourse_endpoint_name():
            continue

        return cc_team_cfg

    raise KeyError(f'No concourse team config for team name {team_name} found')


@ensure_annotations
def client_from_parameters(
    base_url: str,
    password: str,
    team_name: str,
    username: str,
    verify_ssl: bool = True,
    concourse_api_version=None,
):
    """
    returns a concourse-client w/ the credentials valid for the current execution environment.
    The returned client is authorised to perform operations in the same concourse-team as the
    credentials provided calling this function.
    """

    concourse_api = ConcourseApiFactory.create_api(
        base_url=base_url,
        team_name=team_name,
        verify_ssl=verify_ssl,
        concourse_api_version=concourse_api_version,
    )

    concourse_api.login(
        username=username,
        passwd=password,
    )
    return concourse_api


@ensure_annotations
def from_parameters(
    base_url: str,
    password: str,
    team_name: str,
    username: str,
    verify_ssl=True,
    concourse_api_version=None,
):

    concourse_api = ConcourseApiFactory.create_api(
        base_url=base_url,
        team_name=team_name,
        verify_ssl=verify_ssl,
        concourse_api_version=concourse_api_version,
    )

    concourse_api.login(
        username=username,
        passwd=password,
    )
    return concourse_api


@functools.lru_cache()
@ensure_annotations
def from_cfg(
    concourse_cfg: ConcourseConfig,
    team_name: str,
    concourse_uam_cfg: ConcourseUAMConfig=None,
    verify_ssl=True,
    concourse_api_version=None,
):
    # XXX rm last dependency towards cfg-factory
    cfg_factory = ci.util.ctx().cfg_factory()

    concourse_team_config = lookup_cc_team_cfg(
        concourse_cfg_name=concourse_cfg.name(),
        cfg_set=cfg_factory,
        team_name=team_name,
    )
    concourse_endpoint = cfg_factory.concourse_endpoint(
        concourse_team_config.concourse_endpoint_name()
    )
    return client_from_parameters(
        base_url=concourse_endpoint.base_url(),
        password=concourse_team_config.password(),
        team_name=team_name,
        username=concourse_team_config.username(),
    )


@functools.lru_cache()
@ensure_annotations
def from_local_cc_user(
    base_url: str,
    local_cc_user: ConcourseUAM,
    verify_ssl=True,
    concourse_api_version=None,
):

    return from_parameters(
        base_url=base_url,
        password=local_cc_user.password(),
        team_name=local_cc_user.name(),
        username=local_cc_user.username(),
        verify_ssl=verify_ssl,
        concourse_api_version=concourse_api_version,
    )
