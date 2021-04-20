sphinx-rego
===============

A sphinx extension that automatically documents Open Policy Agent Rego policies.

Example:
``` 
.. rego::
   :policy: policies/**/*.rego
   :norecursive:
   :nocustom:
```

Arguments:

_policy_: glob pathname to search for .rego policies with _rego_metadoc_ property

_norecursive_: whether to use glob recursive option

_norecursive_: whether to include custom properties