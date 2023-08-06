from pulumi_google_native.iam.v1 import ServiceAccount, ServiceAccountIamPolicy
from pulumi_google_native.iam import v1
from pulumi import ResourceOptions
import pulumi 
from pulumi import Output

def serviceAccount(stem, parent_res,parent_name, depends_on=None):
        sa = ServiceAccount(
            f'sa-{stem}',
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on),
            account_id='pulumi-deployment',
            display_name=f'sa-{stem}',
            description='This service account is used by pulumi for CICD resource deployment',
            project=parent_name, # parent name needs to be the project name only not including the word 'projects/' that is included in the .name method. Use '._name' instead
        )
        
        # pulumi.export("serviceAccount", sa.email)

        # roles = [
        #         "roles/billing.user",
        #         "roles/compute.networkAdmin",
        #         "roles/compute.xpnAdmin",
        #         "roles/iam.securityAdmin",
        #         "roles/iam.serviceAccountAdmin",
        #         "roles/logging.configWriter",
        #         "roles/orgpolicy.policyAdmin",
        #         "roles/resourcemanager.folderAdmin",
        #         "roles/resourcemanager.organizationViewer"
        #     ]

        return sa

def getServiceAccountIamPolicy(stem, parent_res, project_name, sa_email,depends_on=None):
        sa_binding = ServiceAccountIamPolicy(
            f'binding-{stem}',
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on),
            service_account_id=sa_email,
            project=project_name,
        )
        return sa_binding



def serviceAccountIamPolicy(stem, parent_res, project_name, sa_email, binding, depends_on=None):
        sa_policy = ServiceAccountIamPolicy(
            f'policy-{stem}',
            opts=ResourceOptions(parent=parent_res,depends_on=depends_on),
            service_account_id=sa_email,
            # bindings=[{'condition':None},{'members':[member]},{'role':role}],
            bindings=binding,
            project=project_name,
        )
        return sa_policy

