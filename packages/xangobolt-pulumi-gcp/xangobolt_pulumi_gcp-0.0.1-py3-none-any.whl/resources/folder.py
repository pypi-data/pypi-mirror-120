from pulumi_google_native.cloudresourcemanager.v3 import Folder
from pulumi import ResourceOptions

def folder(stem ,parent_name, depends_on=None):
        fldr = Folder(
            f'fldr-{stem}',
            display_name=f'fldr-{stem}',
            parent = parent_name,
            opts=ResourceOptions(depends_on=depends_on)
        )
        return fldr