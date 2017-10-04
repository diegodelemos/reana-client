# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.
"""REANA client utils."""

import json
import logging

import jsonref
import yaml
from jsonschema import ValidationError, validate

import yadageschemas

from .config import reana_yaml_file_path, reana_yaml_schema_file_path


def yadage_load(workflow_file, toplevel='.'):
    """Validate and return yadage workflow specification.

    :param workflow_file: A specification file compliant with
        `yadage` workflow specification.
    :returns: A dictionary which represents the valid `yadage` workflow.
    """
    import ipdb; ipdb.set_trace()
    res = yadageschemas.load(workflow_file, toplevel=toplevel,
                             schema_name='yadage/workflow-schema',
                             schemadir=yadageschemas.schemadir,
                             validate=True)
    return res


workflow_load = {
    'yadage': yadage_load,
}
"""Dictionary to extend with new workflow specification loaders."""


def load_workflow_spec(workflow_type, workflow_file, **kwargs):
    """Validate and return machine readable workflow specifications.

    :param workflow_type: A supported workflow specification type.
    :param workflow_file: A workflow file compliant with `workflow_type`
        specification.
    :returns: A dictionary which represents the valid workflow specification.
    """
    return workflow_load[workflow_type](workflow_file, **kwargs)


def load_reana_spec():
    """Load and validate reana specification file.

    :raises IOError: Error while reading `reana_yaml_file_path`.
    :raises ValidationError:g `reana_yaml_file_path` does not validate against
        REANA specification.
    """
    try:
        with open(reana_yaml_file_path) as f:
            reana_yaml = yaml.load(f.read())

        _validate_reana_yaml(reana_yaml)
        return reana_yaml
    except IOError as e:
        logging.info(
            'Something went wrong when reading .reana.yaml: {0}'.format(
                e.strerror))
        raise e
    except Exception as e:
        raise e


def _validate_reana_yaml(reana_yaml):
    """Validate REANA specification file according to jsonschema.

    :param reana_yaml: Dictionary which represents `.reana.yaml`.
    :raises ValidationError: `reana_yaml` does not validate against REANA
        specification.
    """
    try:
        with open(reana_yaml_schema_file_path, 'r') as f:
            reana_yaml_schema = json.loads(f.read())

            validate(reana_yaml, reana_yaml_schema)

    except IOError as e:
        logging.info(
            'Something went wrong when reading {0}: {1}'.format(
                reana_yaml_schema_file_path, e.strerror))
        raise e
    except ValidationError as e:
        logging.info('Invalid `.reana.yaml` specification: {0}'.format(
            e.message))
        raise e
