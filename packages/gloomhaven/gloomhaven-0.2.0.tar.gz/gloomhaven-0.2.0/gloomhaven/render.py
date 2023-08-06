import os

from jinja2 import Environment, FileSystemLoader

package_directory = os.path.dirname(os.path.abspath(__file__))
templateLoader = FileSystemLoader(
    searchpath=os.path.join(package_directory, "templates")
)
env = Environment(loader=templateLoader)


def render_table(table):
    template = env.get_template("table.html")
    return template.render(table=table)
