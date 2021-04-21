sphinx-rego Example
===================

We are two _.rego_ [policies](/example/policy), each with their own _metadoc_ properties. Here is one for example:

```rego
package rules.aws.tag

__rego__metadoc__ := {
    "id": "PL203",
    "title": "Resources tags",
    "description": "All AWS resources must have tags",
    "custom": {
        "severity": "High"
    }
}
```

Sphinx-rego extension reads these properties with a simple [policy.rst](/example/docs/policy.rst) command.
Notice that we give a _glob_ pathname to the _:policy: argument, so our two policy files could be in any subdirectory of _policy/_.

```
Policy Documentation
=======================================

.. rego::
   :policy: ../policy/**/*.rego
```

The extension generates documentation accordingly:

![Sphinx Docs](/example/assets/policy.html.png)
