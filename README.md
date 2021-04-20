sphinx-rego
===============

A sphinx extension that automatically documents Open Policy Agent Rego policies using the _rego_metadoc_ property.

# Installation:

Install with PIP

``` commandline
pip3 install sphinx-rego
```

Add to Sphinx `conf.py`
``` python 
extensions += ["sphinxrego.ext"]
```

# Usage Example:
``` 
.. rego::
   :policy: policies/**/*.rego
   :norecursive:
   :nocustom:
```

# Arguments:

_policy_: glob pathname to search for .rego policies with _rego_metadoc_ property

_norecursive_: whether to use glob recursive option

_norecursive_: whether to include custom properties