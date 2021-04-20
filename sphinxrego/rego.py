from typing import Generator

from glob import glob
import os

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from opa import get_metadoc, flatten

import logging


def discover_policies(pathname: str, recursive: bool = False) -> Generator[str, None, None]:
    """
    Use glob to discover .rego policies at pathname
    :param pathname: glob pathname
    :param recursive: glob recursive parameter
    :return: paths to policies
    """
    policies = glob(pathname, recursive=recursive)
    print(f"Found policy files: {policies}")
    for p in policies:
        _, ext = os.path.splitext(p)
        if ext == ".rego":
            yield p


class RegoDirective(Directive):
    has_content = True
    option_spec = {
        "policy": directives.unchanged_required,
        "norecursive": directives.flag,
        "nocustom": directives.flag
    }

    def run(self):
        if "policy" not in self.options:
            raise self.error(":policy: should be specified")

        print(f"{self.__class__.__name__}.run with options: {self.options}")
        recursive = "norecursive" not in self.options
        custom = "nocustom" not in self.options

        all_nodes = []
        for p in discover_policies(self.options["policy"], recursive):
            policy_nodes = self.parse_rego(p, custom)
            all_nodes.extend(policy_nodes)

        print(f"Generated {len(all_nodes)} nodes")
        return all_nodes

    def parse_rego(self, path: str, include_custom: bool = True):
        print(f"Parsing .rego policy at path {path}")

        try:
            meta = get_metadoc(path)
            meta.pop("entrypoints", None)
        except ValueError as e:
            print(str(e))
            self.warning(str(e))
            return []

        items = []

        # title
        section = nodes.section(ids=["Policy:"])
        section += nodes.title(text=meta.get("title", "Policy"))
        items.append(section)

        # description
        if "description" in meta or "id" in meta:
            section = nodes.section(ids=["Description:"])
            section += nodes.title(text="Description")
            if "id" in meta:
                section += nodes.subtitle(text="ID")
                section += nodes.paragraph(text=meta["id"])
            if "description" in meta:
                section += nodes.subtitle(text="Description")
                section += nodes.paragraph(text=meta["description"])
            items.append(section)

        # custom
        if include_custom and "custom" in meta:
            section = nodes.section(ids=["Properties:"])
            section += nodes.title(text="Properties")
            for k, v in flatten(meta).items():
                section += nodes.subtitle(text=k)
                section += nodes.paragraph(text=v)

        print(f"Generated {len(items)} nodes")
        return items


def setup(app):
    app.add_directive("rego", RegoDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
