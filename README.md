# OCI Cross-Tenancy CLI Proxy

## Purpose

This sample presents a solution to use cases where cross-tenancy programmatic manipulation of IAM constructs
is required.

IAM Constructs of Interest:

* Compartments
* Identity Domains
* Groups
* Users
* Policies

## Why is this Needed?  

Due to compliance requirements, a tenancy's IAM security constructs cannot be manipulated directly by an 
external tenancy even if all required cross-tenancy policies are in place.

We can work around that restriction by using an OCI Function to proxy CLI calls within the remote tenancy.
The security aspects of this arrangement are still quite strong, requiring both an instance and resource principal
policy grants.

## Use Case - Cross-Tenancy infrastructure-as-code (IaC)

OCI supports a fully-managed / hosted Terraform via its Resource Manager Service.  That service provides
the full range of API access as implemented by the oci-provider.

Organizations frequently want to have one OCI tenancy serve as an IaC `Control Plane` that can manage remote tenancies
which are either customer-accessible or customer-owned. 

OCI cross-tenancy policies allow for this type of relationship thereby avoiding the need to share account keys
across tenancies.  

## Architecture

![resource-manager-use-case](images/resource-manager-use-case.png)

---
# Remote Tenancy Setup

to do ...

## Remote Compartment

to do ...


## Instance Principal Dynamic Group

to do ...


## Cross-Tenancy Policy

to do ...


---

# Controller Tenancy Setup

to do ...


## Controller Compartment

to do ...


## Resource Principal Dynamic Group

to do ...


## Cross-Tenancy Policy

to do ...


## CLI Proxy Function

to do ...


----
# Testing

phx-proxy-app
* The Fn application name.
* Note that your application MUST BE IN THE HOME REGION to perform IAM manipulations.
* This one is in Phoenix region (hence the phx prefix).

oci-cli-proxy
* The Fn function name.

--auth resource_principal
* This is added by the CLI Proxy Function if not present.

Export these remote tenancy OCIDs for convenience:

    export TENANCY_ID=ocid1.tenancy.oc1.phx...
    export COMP_ID=ocid1.compartment.oc1.phx...
    export FN_ID=ocid1.fnfunc.oc1.phx...


## Object Storage Namespace

Invoke via cli:

    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci os ns get-metadata'

Invoke via fn:

    echo -n 'oci os ns get-metadata' | fn invoke phx-proxy-app oci-cli-proxy

## List Compartments

    echo -n 'oci iam compartment list --compartment-id $COMP_ID' |fn invoke amdocs-phx-app oci-cli-proxy
    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci iam compartment list --compartment-id $($COMP_ID)'

## List Compartment at Root 

    echo -n 'oci iam compartment list --compartment-id $TENANCY_ID' |fn invoke amdocs-phx-app oci-cli-proxy
    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci iam compartment list --compartment-id $($TENANCY_ID)'


## Create a Compartment

    echo -n 'oci iam compartment create --name test-compartment-1 --description testing --compartment-id $COMP_ID' | fn invoke amdocs-phx-app oci-cli-proxy
    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci iam compartment create --compartment-id $($COMP_ID) --name test-compartment-1 --description testing'

----
# Infrastructure as Code

## List Architecture Types (Category 2)

    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci resource-manager template list --all --compartment-id $($COMP_ID) --template-category-id 2'

## Create a Resource Manager Stack from Template

    export TEMPLATE_ID=ocid1.ormtemplate.oc1.phx...
    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci resource-manager stack create-from-template --compartment-id  $($COMP_ID)  --template-id $($TEMPLATE_ID) --terraform-version 1.0.x'

## Update Resource Manager Stack Variables

See [handling JSON with CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliusing.htm#ManagingCLIInputandOutput)

    export STACK_ID=ocid1.ormstack.oc1.phx...
    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci resource-manager stack update --stack-id $($STACK_ID) --force --variables "{\"resource_label\":\"example\"}"'
    oci fn function invoke --function-id $FN_ID --file "-" --body "oci resource-manager stack update --stack-id $($STACK_ID) --force --variables '{\"resource_label2\":\"example2\"}'"

use this to serialize a JSON file of variables found in a local file variables.json:

    oci fn function invoke --function-id $FN_ID --file "-" --body "oci resource-manager stack update --stack-id $($STACK_ID) --force --variables $(python serialize.py variables.json 2>&1)"

## Create a Resource Manager Plan Job

    oci fn function invoke --function-id $FN_ID --file "-" --body 'oci resource-manager job create-plan-job --stack-id $($STACK_ID)'

## Run Plan Job

to do ...



## Create a Resource Manager Apply Job

to do ...




## Run Apply Job

to do ...




## Create a Resource Manager Delete Job

to do ...




## Run Delete Job

to do ...


----
