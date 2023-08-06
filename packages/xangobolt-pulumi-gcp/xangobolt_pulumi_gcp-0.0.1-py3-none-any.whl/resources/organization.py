from pulumi_google_native.cloudresourcemanager.v3 import OrganizationIamPolicy
from pulumi_google_native.cloudresourcemanager import v3
from pulumi_google_native.cloudbilling.v1 import BillingAccountIamPolicy
from pulumi_google_native.cloudbilling import v1
from pulumi import ResourceOptions

def getOrganizationIamPolicy(stem,org_id,depends_on=None):
        org_iam = v3.get_organization_iam_policy(
            organization_id=org_id
        )
        return org_iam



def setOrganizationIamPolicy(stem,org_id,binding,parent_res,depends_on=None):
        # print(binding)
        org_iam = OrganizationIamPolicy(
            f'policy-{stem}',
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on),
            # bindings=[{'condition':None},{'members':[member]},{'role':role}],
            bindings=binding,
            organization_id=org_id
        )
        return org_iam


def getBillingIamPolicy(stem,acct_id,depends_on=None):
        org_iam = v1.get_billing_account_iam_policy(
            billing_account_id=acct_id
        )
        return org_iam


def setBillingIamPolicy(stem,acct_id,binding,parent_res, depends_on=None):
        org_iam = BillingAccountIamPolicy(
            f'policy-{stem}',
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on),
            # bindings=[{'condition':None},{'members':[member]},{'role':role}],
            bindings=binding,
            billing_account_id=acct_id
        )
        return org_iam