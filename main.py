import json
from dotenv import dotenv_values

import pyaem2

from helpers.aem import AEMClient, local_install_package
from helpers.package_names_and_filters import PACKAGE_NAMES_AND_FILTERS


config = dotenv_values(".env")

AEM_DEV_URL = config["DEV_HOST"]
LOGIN_TOKEN = config["LOGIN_TOKEN"]
GROUP_NAME = "my_packages"
VERSION = "1.0.0"


def main():
    # Create an AEM client instance
    dev = AEMClient(AEM_DEV_URL, LOGIN_TOKEN, local=False)
    user = config["LOCAL_USER"]
    password = config["LOCAL_PASSWORD"]
    local = pyaem2.PyAem2(user, password, "localhost", 4502)

    for package_name, filter in PACKAGE_NAMES_AND_FILTERS:
        print(f"Starting process for {package_name} (with filter {filter})")
        package_path = f"/etc/packages/{GROUP_NAME}/{package_name}.zip"
        download_path = f"{package_name}-1.0.0.zip"

        # Step 1: Create the package
        dev.create_package(package_name, GROUP_NAME, VERSION)

        # Step 2: Modify filters (example: adding /content/my-site filter)
        filters = [{"root": filter, "rules": []}]
        dev.update_package_filters(package_path, package_name, GROUP_NAME, filters)

        # Step 3: Build and install the package
        dev.build_package(package_path)

        # Step 4: Download the package
        dev.download_package(package_path, download_path)

        # Step 5: Upload the package (after modifying)
        result = local.upload_package(
            GROUP_NAME, package_name, VERSION, ".", force="true"
        )
        if result.is_failure():
            print(json.dumps({"failed": True, "msg": result.message}))
        else:
            print(json.dumps({"msg": result.message}))

        # Step 6: Install the newly uploaded package
        print("Installing package")
        local_install_package(
            "http://admin:admin@localhost:4502",
            group_name=GROUP_NAME,
            package_name=package_name,
        )

        print("🎉 Package created, modified, and installed successfully!")


if __name__ == "__main__":
    main()
