from pulumi_google_native.servicemanagement.v1 import Service
from pulumi import ResourceOptions

def service(stem, parent_res, proj , apiservice, depends_on=None):
        bkt = Service(
            f'apiservice-{stem}',
            service_name=apiservice,
            producer_project_id=proj,
            opts=ResourceOptions(parent=parent_res,delete_before_replace=True,depends_on=depends_on)
        )
        return bkt