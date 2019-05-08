"""
    Copyright 2016 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import uuid

import pytest


@pytest.mark.asyncio
async def test_project_api(client):
    result = await client.create_project("project-test")
    assert result.code == 200
    assert "project" in result.result
    assert "id" in result.result["project"]

    project_id = result.result["project"]["id"]

    result = await client.create_project("project-test")
    assert result.code == 500

    result = await client.list_projects()
    assert result.code == 200
    assert "projects" in result.result
    assert len(result.result["projects"]) == 1

    assert result.result["projects"][0]['id'] == project_id

    result = await client.get_project(id=project_id)
    assert result.code == 200
    assert "project" in result.result
    assert result.result["project"]['id'] == project_id
    assert result.result["project"]['name'] == "project-test"

    result = await client.modify_project(id=project_id, name="project-test2")
    assert result.code == 200
    assert "project" in result.result
    assert result.result["project"]['id'] == project_id
    assert result.result["project"]['name'] == "project-test2"

    result = await client.get_project(id=project_id)
    assert result.code == 200
    assert "project" in result.result
    assert result.result["project"]['id'] == project_id
    assert result.result["project"]['name'] == "project-test2"

    result = await client.delete_project(id=project_id)
    assert result.code == 200

    result = await client.list_projects()
    assert result.code == 200
    assert "projects" in result.result
    assert len(result.result["projects"]) == 0


@pytest.mark.asyncio
async def test_env_api(client):
    result = await client.create_project("env-test")
    assert result.code == 200
    assert "project" in result.result
    assert "id" in result.result["project"]
    project_id = result.result["project"]["id"]

    result = await client.create_environment(project_id=project_id, name="dev")
    assert result.code == 200
    assert "environment" in result.result
    assert "id" in result.result["environment"]
    assert "project" in result.result["environment"]
    assert project_id == result.result["environment"]["project"]
    assert "dev" == result.result["environment"]["name"]

    env_id = result.result["environment"]["id"]

    result = await client.modify_environment(id=env_id, name="dev2")
    assert result.code == 200
    assert "environment" in result.result
    assert result.result["environment"]['id'] == env_id
    assert result.result["environment"]['name'] == "dev2"

    result = await client.get_environment(id=env_id)
    assert result.code == 200
    assert "environment" in result.result
    assert result.result["environment"]['id'] == env_id
    assert result.result["environment"]['project'] == project_id
    assert result.result["environment"]['name'] == "dev2"

    project_result = await client.get_project(id=project_id)
    assert project_result.code == 200
    assert "project" in project_result.result
    assert env_id in project_result.result["project"]["environments"]

    result = await client.list_environments()
    assert result.code == 200
    assert len(result.result) == 1

    result = await client.delete_environment(id=env_id)
    assert result.code == 200

    result = await client.list_environments()
    assert result.code == 200
    assert "environments" in result.result
    assert len(result.result["environments"]) == 0


@pytest.mark.asyncio
async def test_project_cascade(client):
    result = await client.create_project("env-test")
    project_id = result.result["project"]["id"]

    result = await client.create_environment(project_id=project_id, name="dev")
    result = await client.create_environment(project_id=project_id, name="prod")

    result = await client.delete_project(project_id)
    assert result.code == 200

    result = await client.list_environments()
    assert len(result.result["environments"]) == 0


@pytest.mark.asyncio
async def test_create_with_id(client):
    project_id = uuid.uuid4()
    result = await client.create_project(name="test_project", project_id=project_id)
    assert result.result["project"]["id"] == str(project_id)

    env_id = uuid.uuid4()
    result = await client.create_environment(project_id=project_id, name="test_env", environment_id=env_id)
    env = result.result["environment"]
    assert env["id"] == str(env_id)
    assert env["project"] == str(project_id)

    result = await client.create_environment(project_id=project_id, name="test_env2", environment_id=env_id)
    assert result.code == 500
