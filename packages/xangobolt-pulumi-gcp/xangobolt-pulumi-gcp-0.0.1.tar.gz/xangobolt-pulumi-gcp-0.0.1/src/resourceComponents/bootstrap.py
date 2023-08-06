from pulumi import ComponentResource, ResourceOptions, StackReference
from resources import folder,project,serviceAccount,organization, cloudStorage, apiService
import pulumi
from pulumi import Output

class Bootstrap(ComponentResource):
    def __init__(self, name: str, props: None, opts:  ResourceOptions = None):
        super().__init__('Bootstrap', name, {}, opts)

        self.prefix = props.prefix
        self.domain = props.domain
        self.separator = props.separator
        self.env = props.env
        self.tags = props.tags
        self.suffix = props.suffix
        self.location = props.location

        # Create Bootstrap folder 
        fldr = folder.folder('bootstrap-dev', 'organizations/724960081576')


        
        # In this section, we are creating the CICD Project and associated resources:
            # 1) Create SEED Project
            # 2) Enable APIs for seed project
            # 3) Create Deployment Service Account
            # 4) Assign ORG level permissions for org_admin, billing_admin groups and service account
            # 5) Assign Billing level permissions for service account
            # 6) Create State Storage Bucket for pulumi backend

        # Create seed project
        prj_seed = project.project('seed-dev', fldr, fldr.name)

        # Enable/Activate Service APIs in the Seed project
        seed_apis = [
            "serviceusage.googleapis.com",
            "servicenetworking.googleapis.com",
            "compute.googleapis.com",
            "logging.googleapis.com",
            "bigquery.googleapis.com",
            "cloudresourcemanager.googleapis.com",
            "cloudbilling.googleapis.com",
            "iam.googleapis.com",
            "admin.googleapis.com",
            "appengine.googleapis.com",
            "storage-api.googleapis.com",
            "monitoring.googleapis.com"
            ]

        for api in seed_apis:
            activate_api = apiService.service(f'api-{api}', prj_seed, prj_seed._name, api)

        # Create Pulumi Resource deployment service account
        sa_pulumi = serviceAccount.serviceAccount('pulumi', prj_seed, prj_seed._name)

        # ASSIGN PERMISSIONS AT ORGANIZATION LEVEL
        # Get IAM policy for the Organization resource
        org_iam_policy = organization.getOrganizationIamPolicy('org iam', '724960081576') # Organization ID should be a config input to the bootstrap module

        billing_admin_group = 'gcp-billing-admins' #this should be a cinfig input to the bootstrap module
        org_admin_group = 'gcp-organization-admins' #this should be a cinfig input to the bootstrap module
        sa_member = Output.concat('serviceAccount:', sa_pulumi.email)
        

        # Billing roles for admin
        billing_admin_org_iam_permissions = [
            "roles/billing.admin",
            "roles/billing.creator"
            ]

        # Append billing roles to organization level iam policy for billing admin group
        for role in billing_admin_org_iam_permissions:
            binding = {"members": [billing_admin_group], "role": role}
            org_iam_policy.bindings.append(binding)

        #Org Admin roles
        org_admins_org_iam_permissions = [
            "roles/billing.user",
            "roles/resourcemanager.organizationAdmin"
            ]

        # Append org admin roles to organization level iam policy for org admin group
        for role in org_admins_org_iam_permissions:
            binding = {"members": [org_admin_group], "role": role}
            org_iam_policy.bindings.append(binding)


        # Service Account roles
        sa_org_iam_permissions = [
            "roles/billing.user",
            "roles/compute.networkAdmin",
            "roles/compute.xpnAdmin",
            "roles/iam.securityAdmin",
            "roles/iam.serviceAccountAdmin",
            "roles/logging.configWriter",
            "roles/orgpolicy.policyAdmin",
            "roles/resourcemanager.folderAdmin",
            "roles/resourcemanager.organizationViewer"
            ]

        # Append service account roles to organization level iam policy for the deployment service account
        for role in sa_org_iam_permissions:
            binding = {"members": [sa_member], "role": role}
            org_iam_policy.bindings.append(binding)

        # Update IAM policy for the organization resource with new role bindings
        organization.setOrganizationIamPolicy('org_iam', '724960081576', org_iam_policy.bindings, prj_seed)


        # ASSIGN PERMISSIONS AT BILLING ACCOUNT LEVEL
        # Get IAM policy for the billing account
        billing_iam_policy = organization.getBillingIamPolicy('billing_iam', '0117D4-F2485F-1589A0') # Billing Account ID should be a config input to the bootstrap module
        

        # Billing roles for user
        billing_user_org_iam_permissions = [
            "roles/billing.user"
            ]

        # Append billing roles to billing account level iam policy for deployment service account
        for role in billing_user_org_iam_permissions:
            binding = {"members": [sa_member], "role": role}
            org_iam_policy.bindings.append(binding)

        # Update IAM policy for the billing account resource with new role bindings
        organization.setBillingIamPolicy('billing_iam', '0117D4-F2485F-1589A0', billing_iam_policy.bindings, prj_seed)

        
        # Create Pulumi Backend Storage for state management using Cloud Storage
        seed_bucket = cloudStorage.bucket('seedBucket',prj_seed, prj_seed._name)

        # ASSIGN PERMISSIONS AT CLOUD STORAGE LEVEL
        # Get IAM policy for the Cloud storage bucket
        bucket_iam_policy = [{}]

        # Bucket roles for service account
        billing_user_org_iam_permissions = [
            "roles/storage.admin"
            ]

        # Append billing roles to billing account level iam policy for deplotment service account
        for role in billing_user_org_iam_permissions:
             binding = {"members": [sa_member], "role": role}
             bucket_iam_policy.append(binding)

        # Update IAM policy for the cloud storage resource with new role bindings
        cloudStorage.setStorageIamPolicy('bucket_iam', seed_bucket.name, bucket_iam_policy, seed_bucket)

        


        # In this section, we are creating the CICD Project and associated resources
            # 1) Create CICD Project
            # 2) Create CIDC Build trigger?
        
        # Create CICD project
        prj_cicd = project.project('cicd-dev', fldr, fldr.name)

        billing_admin_org_iam_permissions = [
            "roles/billing.admin",
            "roles/billing.creator"
            ]
        
        # Create CloudBuild Pipeline


