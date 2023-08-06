import json
from typing import Dict, Tuple
import requests

class ReadTheDocsUploader(object):

    def __init__(self, token: str):
        self.read_the_docs_url = "https://readthedocs.org/api/v3/"
        self.token = token

    def generate_new_documentation(self, project_name: str, repository_url: str, project_homepage: str, repository_type: str = "git", programming_language: str = "py", language: str = "en", project_version: str = None):
        if not self._is_project_present(project_name):
            self._create_project_with(
                name=project_name,
                repository_url=repository_url,
                repository_type=repository_type,
                project_homepage=project_homepage,
                programming_language=programming_language,
                language=language
            )
        # trigger build on readthedocs
        self._generate_new_build(
            project_name=project_name,
            project_version=project_version
        )

    def _generate_new_build(self, project_name: str, project_version: str = None):
        if project_version is None:
            project_version = "latest"
        response, _, body = self._contact_readthedocs_endpoint(
            method="POST",
            query_url=f"projects/{project_name}/versions/{project_version}/builds/"
        )

    def _contact_readthedocs_endpoint(self, method: str, query_url: str, query_params: Dict[str, str] = None, body: Dict[str, any] = None, check_status: bool = True) -> Tuple[any, int, any]:
        if query_url.startswith("/"):
            query_url = query_url[1:]
        url = f"{self.read_the_docs_url}{query_url}"

        response = requests.request(
            method=method,
            url=url,
            params=query_params,
            headers={
                "Authorization": f"token {self.token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(body, indent=2),
        )
        if check_status:
            try:
                response.raise_for_status()
            except:
                raise ValueError("\n".join([
                    f"URL={url}",
                    f"request body={json.dumps(body, indent=2)}",
                    f"response status={response.status_code}",
                    f"response body={json.dumps(response.json(), indent=2)}",
                ]))

        return response, response.status_code, response.json()

    def _is_project_present(self, project_name: str) -> bool:
        """
        Check if the project is already present on your account

        :param project_name: project of the name to find
        :return:
        """
        response, status_code, body = self._contact_readthedocs_endpoint(
            method="GET",
            query_url="projects/",
        )
        return len(list(filter(lambda project: project["name"] == project_name, body["results"]))) > 0

    def _create_project_with(self, name: str, repository_url: str, repository_type: str, project_homepage: str, programming_language: str, language: str):
        """
        Create

        :param name: name fo the project
        :param repository_url: version control url for the project
        :param repository_type: git, svn or something else
        :param project_homepage: homepage of the project
        :param programming_language: py or something else
        :param language: it, es, en or something else

        ..::seealso:: https://docs.readthedocs.io/en/stable/api/v3.html#project-create
        :return:
        """
        json_data = dict(
            name=name,
            repository=dict(
                url=repository_url,
                type=repository_type,
            ),
            homepage=project_homepage,
            programming_language=programming_language,
            language=language,
        )
        return self._create_project(json_data)

    def _create_project(self, json_data):
        response, status_code, body = self._contact_readthedocs_endpoint(
            method="POST",
            query_url="projects/",
            body=json_data
        )




if __name__ == "__main__":
    p = ReadTheDocsUploader(token="e085af1ef5f01f286f2260984649d44004e5796d")
    p.generate_new_documentation(
        project_name="readthedocs-uploader",
        repository_url="https://github.com/Koldar/django-koldar-common-apps",
        project_homepage="https://github.com/Koldar/django-koldar-common-apps",
    )
