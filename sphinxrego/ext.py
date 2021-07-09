from typing import Generator

from glob import glob
import os

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinxrego.opa import discover_policies

import logging


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

        logging.debug(f"{self.__class__.__name__}.run with options: {self.options}")
        recursive = "norecursive" not in self.options
        include_custom = "nocustom" not in self.options

        all_nodes = []
        for p, meta, custom in discover_policies(self.options["policy"], recursive):
            policy_nodes = self.parse_rego(p, meta, custom, include_custom)
            all_nodes.extend(policy_nodes)

        logging.debug(f"Generated {len(all_nodes)} nodes")
        return all_nodes

    def parse_rego(self, path: str, meta: dict, custom: dict, include_custom: bool = True):
        """
        :param path: path to rego file
        :param meta: __rego_metadoc__ main properties
        :param custom: __rego_metadoc__ custom properties
        :param include_custom: whether to include custom properties
        """
        logging.debug(f"Parsing .rego policy at path {path}")

        root = nodes.section(ids=[meta["title"], ])
        root += nodes.title(text=meta["title"])

        # description
        if "description" in meta or "id" in meta:
            if "id" in meta:
                section = nodes.section(ids=[f"{meta['title']}-ID", ])
                section += nodes.subtitle(text="ID")
                section += nodes.paragraph(text=meta["id"])
                root += section
            if "description" in meta:
                section = nodes.section(ids=[f"{meta['title']}-desc", ])
                section += nodes.subtitle(text="Description")
                section += nodes.paragraph(text=meta["description"])
                root += section

        # custom
        if include_custom:
            for k, v in custom.items():
                section = nodes.section(ids=[f"{meta['title']}-{k}", ])
                section += nodes.subtitle(text=k)
                section += nodes.paragraph(text=v)
                root += section

        logging.debug(f"Generated {len(root)} nodes")
        return [root, ]


def setup(app):
    app.add_directive("rego", RegoDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
