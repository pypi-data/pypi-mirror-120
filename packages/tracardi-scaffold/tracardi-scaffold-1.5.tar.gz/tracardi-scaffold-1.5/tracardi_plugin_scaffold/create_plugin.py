import os
import zipfile
from jinja2 import Template


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


print("Plug-in name will become its package and PiPy package name.")
plugin_name = get("Plug-in name > ")

package = plugin_name.replace(" ", "_")
package_name = plugin_name.replace(" ", "-")

print("Describe what plug-in odes in one sentence.")
plugin_description = get("Plug-in on line description > ")
plugin_author = get("Plug-in author > ")
plugin_author_email = get("Plug-in author email> ")
plugin_class = get("Plugin class > ")

with zipfile.ZipFile(os.path.join(local_dir,'plugin_scaffold.zip'), 'r') as zip_ref:
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

os.rename(f"{location}/plugin", f"{location}/{package}")

print("Please:")
print("- run pip install -r requirements.txt")
print(f" - do to folder {location} where you will find your plugin.")