#!/usr/bin/env python3
import shutil

from python_utils import ROOT, colors


class placeholders:
    name: str = "<<NAME_PLACEHOLDER>>"
    vendor: str = "<<VENDOR_PLACEHOLDER>>"
    docker: str = "<<DOCKER_REPO_PLACEHOLDER>>"
    github: str = "<<GITHUB_REPO_PLACEHOLDER>>"
    description: str = "<<DESCRIPTION_PLACEHOLDER>>"


MANIFEST_TEMPLATE = f"""APP_NAME="{placeholders.name}"
APP_VENDOR="{placeholders.vendor}"
APP_DOCKER_REPO="{placeholders.docker}"
APP_GITHUB_REPO="{placeholders.github}"
APP_DESCRIPTION="{placeholders.description}"
"""


def askfor(
    name: str,
    prompt: str,
    example: str = "",
    color: str = colors.blue,
    required: bool = True,
) -> str:
    var = input(
        f"{prompt} "
        f"{color}[e.g. {example}]{colors.reset} "
        f"[{'required' if required else 'not required'}] >>> "
    )
    if not var and required:
        raise SystemExit(f"{colors.red}you must provide {name!r}")
    return var


if __name__ == "__main__":
    # Interactively ask user for the necessary variables
    print(f"{colors.green}Initializing new flask repo...{colors.reset}")
    name = askfor("name", "Application name", example="my-app")
    vendor = askfor("vendor", "Vendor name", example="your company")
    docker_repo = askfor(
        "docker_repo",
        "Docker repo",
        example="dockerhub.io/test/testimage",
        required=False,
    )
    github_repo = askfor(
        "github_repo",
        "Github repo",
        example="github.com/bamaxw/flask-template",
        required=False,
    )
    description = askfor(
        "description",
        "Application description",
        example="general purpose etc",
        required=False,
    )

    manifest_path = f"{ROOT}/manifest.sh"
    new_manifest_contents = (
        MANIFEST_TEMPLATE.replace(placeholders.name, name)
        .replace(placeholders.vendor, vendor)
        .replace(placeholders.docker, docker_repo)
        .replace(placeholders.github, github_repo)
        .replace(placeholders.description, description)
    )
    with open(manifest_path, "w") as manifest:
        manifest.write(new_manifest_contents)
        manifest.flush()

    # Move lib -> new repo name
    # Move this file to __alreadyinitialized.py
    new_src_dir = name.replace("-", "_").strip('"')
    shutil.move(f"{ROOT}/libcontents", f"{ROOT}/{new_src_dir}")
    shutil.move(f"{ROOT}/scripts/init.py", f"{ROOT}/scripts/__alreadyinitialized.py")
