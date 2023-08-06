from pulumi_google_native.cloudresourcemanager.v3 import Project
from pulumi import ResourceOptions

def project(stem, parent_res ,parent_name, depends_on=None):
        proj = Project(
            f'prj-{stem}',
            display_name=f'prj-{stem}',
            project=f'prj-{stem}',
            parent = parent_name,
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on)
        )
        return proj