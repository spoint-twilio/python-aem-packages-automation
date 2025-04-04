import unicodedata
from typing import Any

import pycurl
import requests


def local_install_package(url, group_name: str, package_name: str) -> None:
    payload = {"cmd": "install", "recursive": "true"}
    url = "{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}.zip".format(
        url, group_name, package_name
    )
    response = requests.post(url, data=payload)
    print(response.json())


class AEMClient:
    def __init__(self, aem_url: str, login_token: str, local: bool = False) -> None:
        self.aem_url = aem_url
        self.session = requests.Session()
        if not local:
            self.cookies = {"login-token": login_token}
            self.session.cookies.update(self.cookies)
        else:
            self.cookies = {}

    def create_package(self, package_name: str, group_name: str, version: str) -> None:
        print(f"Creating package {package_name}...")
        url = f"{self.aem_url}/crx/packmgr/service/.json"
        data = {
            "cmd": "create",
            "packageName": package_name,
            "groupName": group_name,
            "version": version,
            "_charset_": "utf-8",
        }
        response = self.session.post(url, data=data)
        print(response.json())

    def delete_package(self, package_path: str) -> None:
        print(f"Deleting package {package_path}...")
        url = f"{self.aem_url}/crx/packmgr/service/.json{package_path}"
        data = {"cmd": "delete"}
        response = self.session.post(
            url, data=data, timeout=70
        )  # a timeout of a bit more than 1 minute, which seems to be the timeout on the server side
        print(response.json())

    def download_package(self, package_path: str, download_path: str) -> None:
        print(f"Downloading package from {package_path}...")
        url = f"{self.aem_url}{package_path}"
        response = self.session.get(url)

        if response.status_code == 200:
            with open(download_path, "wb") as file:
                file.write(response.content)
            print(f"Package downloaded to {download_path}.")
        else:
            print(f"Failed to download package. Status Code: {response.status_code}")

    def upload_package(self, package_path: str, package_file_path: str) -> None:
        print(f"Uploading package {package_path}...")
        url = f"{self.aem_url}/crx/packmgr/service/.json"
        data = {
            "cmd": "upload",
            "package": (pycurl.FORM_FILE, package_file_path),
        }  # packagePath to specify where the package is stored
        response = self.session.post(url, data=data)
        print(response.json())

    def build_package(self, package_path: str) -> None:
        print(f"Building package {package_path}...")
        url = f"{self.aem_url}/crx/packmgr/service/.json{package_path}"
        data = {"cmd": "build"}
        response = self.session.post(
            url, data=data, timeout=70
        )  # a timeout of a bit more than 1 minute, which seems to be the timeout on the server side
        print(response.json())

    def install_package(self, package_path: str) -> None:
        print(f"Installing package {package_path}...")
        url = f"{self.aem_url}/crx/packmgr/service/.json{package_path}"
        data = {"cmd": "install"}
        response = self.session.post(url, data=data)
        print(response.json())

    def update_package_filters(
        self,
        package_path: str,
        package_name: str,
        group_name: str,
        filters: list[dict[str, str | list[Any]]],
    ) -> None:
        print(f"Editing package filters for {package_path}...")

        # Send a POST request to get the current package metadata
        url = f"{self.aem_url}/crx/packmgr/update.jsp"
        encoded_path = unicodedata.normalize("NFKD", package_path).encode(
            "ascii", "ignore"
        )
        payload = {
            "packageName": (None, package_name),
            "groupName": (None, group_name),
            "path": (None, encoded_path),
            "filter": (None, str(filters)),
            "acHandling": (None, "merge"),
        }
        response = self.session.post(url, files=dict(foo="bar"), data=payload)
        print(response.json())
