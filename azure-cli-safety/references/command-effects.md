# Examples that defeat name-based checks

These examples illustrate effects, not a complete allow-list. Recheck the exact
command, parameters, credential path, and surrounding shell before use.

| Command or pattern | Classification and reason |
| --- | --- |
| `az vm show`, `az resource list` | `READ` when limited to inspection with verified context and no surrounding writes. |
| `az storage message get` | **NON-READ**: receiving changes queue-message visibility/processing state. A verified `az storage message peek` is the passive alternative, subject to scope and credential checks. See [storage messages](https://learn.microsoft.com/en-us/cli/azure/storage/message). |
| `az aks get-credentials` with its default/file destination | **NON-READ**: merges credentials into a local Kubernetes configuration; `--overwrite-existing` can replace an entry. See [get-credentials](https://learn.microsoft.com/en-us/cli/azure/aks#az-aks-get-credentials). |
| `az storage blob download`, `azcopy copy` downloads, `... > file`, `... \| tee file` | **NON-READ**: local creation/overwrite counts. Uploads and service-to-service copies also write. |
| `azcopy sync ... --delete-destination=true` | **NON-READ**, **DESTRUCTIVE**: copies and can delete destination files/blobs. Review `--dry-run` separately, including local log/job-file effects. See [AzCopy sync](https://github.com/Azure/azure-storage-azcopy/wiki/azcopy_sync). |
| `az deployment group what-if` | May be `READ` only after checking the exact preview and local prerequisites; it predicts resource changes without applying them. Permissions may still be required; do not grant them to unblock inspection. See [what-if](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deploy-what-if). |
| `az deployment group create --confirm-with-what-if` | **NON-READ**: can proceed from preview into deployment. A confirmation prompt does not make it a read. See [what-if deployment commands](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deploy-what-if). |
| `az login`, `az account set`, `az configure`, extension/Bicep installation | **NON-READ**: session, configuration or tool-installation changes need a plan. See [authentication](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli). |
| VM run-command, restarts, workload/job starts, resource changes | **NON-READ**: execution or state changes. `--yes`, `--no-wait` and `--only-show-errors` do not make a command a preview or provide authorisation. |
