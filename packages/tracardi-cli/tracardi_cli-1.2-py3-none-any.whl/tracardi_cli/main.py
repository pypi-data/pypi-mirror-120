import os
import zipfile

from jinja2 import Template
import argparse

local_dir = os.path.dirname(os.path.realpath(__file__))


def get(label):
    string = ""
    while string == "":
        string = input(f"{label}")
    return string


def replace(file, replacements):
    with open(file, "r") as f:
        content = f.read()
        t = Template(content)
        content = t.render(**replacements)
        with open(file, "w") as w:
            w.write(content)
            print(f"File {file} created.")


def logo():
    print("""
 ____   __    ___    __    ____  ____  ____ 
(_  _) /__\  / __)  /__\  (  _ \(  _ \(_  _)
  )(  /(__)\( (__  /(__)\  )   / )(_) )_)(_ 
 (__)(__)(__)\___)(__)(__)(_)\_)(____/(____)""")


def cli():
    logo()

    print("Command line interface")
    print()

    parser = argparse.ArgumentParser(description='Tracardi CLI.')
    parser.add_argument('--plugin', type=str, nargs=1,
                        help='Type of plugin action eg. scaffold')

    args = parser.parse_args()

    if args and 'plugin' in args:
        if isinstance(args.plugin, list) and 'scaffold' in args.plugin:
            print("PLUGIN SCAFFOLD")
            print("Please type the following information.")
            print("-----------------------------------------------------")
            print()
            print("Plug-in name will become its package and PiPy package name.")
            plugin_name = get("Plug-in name > ")

            package = plugin_name.replace(" ", "_")
            package_name = plugin_name.replace(" ", "-")

            print("Describe what plug-in odes in one sentence.")
            plugin_description = get("Plug-in on line description > ")
            plugin_author = get("Plug-in author > ")
            plugin_author_email = get("Plug-in author email > ")
            plugin_class = get("Plugin class > ")

            with zipfile.ZipFile(os.path.join(local_dir, 'plugin_scaffold.zip'), 'r') as zip_ref:
                zip_ref.extractall(".")

            replacements = {
                "plugin_name": package_name,
                "plugin_description": plugin_description,
                "plugin_package": package,
                "plugin_class": plugin_class,
                "plugin_author": plugin_author,
                "plugin_author_email": plugin_author_email
            }

            location = "."
            replace(f"{location}/MANIFEST.in", replacements)
            replace(f"{location}/LICENSE.md", replacements)
            replace(f"{location}/setup.py", replacements)
            replace(f"{location}/build.sh", replacements)
            replace(f"{location}/plugin/plugin.py", replacements)
            replace(f"{location}/test/manual_test.py", replacements)

            os.rename(f"{location}/plugin", f"{location}/{package}")

            print("Please:")
            print("- RUN: pip install -r requirements.txt")
            print(f" - GO TO: folder {location} where you will find your plugin.")


if __name__ == "__main__":
    cli()
