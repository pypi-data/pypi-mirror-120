from pulumi_google_native.storage import v1
from pulumi import ResourceOptions

def bucket(stem, parent_res, proj, depends_on=None):
        bkt = v1.Bucket(
            f'bkt-{stem}',
            name=f'bkt-{stem}',
            project=proj,
            versioning=True,
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on)
        )
        return bkt

def getBucketIamPolicy(bucket_id,proj,depends_on=None):
        bkt_iam = v1.get_bucket_iam_policy(
            bucket=bucket_id,
            user_project=proj
        )
        return bkt_iam


def setStorageIamPolicy(stem,bucket_id,binding,parent_res,depends_on=None):
        org_iam = v1.BucketIamPolicy(
            f'policy-{stem}',
            bucket=bucket_id,
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on),
            bindings=binding
        )
        return org_iam