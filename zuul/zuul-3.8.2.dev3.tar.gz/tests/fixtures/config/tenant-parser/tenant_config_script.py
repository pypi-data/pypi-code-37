#!/usr/bin/env python

tenant_config = """---
- tenant:
    name: tenant-one
    source:
      gerrit:
        config-projects:
          - common-config
        untrusted-projects:
          - org/project1
          - org/project2
"""

print(tenant_config)
