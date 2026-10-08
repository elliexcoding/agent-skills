# Examples that defeat name-based checks

These examples illustrate effects, not a complete allow-list. Recheck the exact
command, parameters, credential path, and surrounding shell before use.

| Command or pattern | Classification and reason |
| --- | --- |
| `gcloud compute instances list`, `gcloud projects describe` | `READ` when limited to inspection with verified context and no surrounding writes. |
| `gcloud pubsub subscriptions pull` | **NON-READ** even without `--auto-ack`: delivery affects acknowledgement deadlines and redelivery state. `--auto-ack` also acknowledges messages. See [pull](https://docs.cloud.google.com/sdk/gcloud/reference/pubsub/subscriptions/pull) and [delivery state](https://docs.cloud.google.com/pubsub/docs/reference/rest/v1/projects/subscriptions/pull). |
| `gcloud container clusters get-credentials` | **NON-READ**: updates the local Kubernetes configuration. See [get-credentials](https://docs.cloud.google.com/sdk/gcloud/reference/container/clusters/get-credentials). |
| `gcloud storage cp` / `gsutil cp` downloads, `... > file`, `... \| tee file` | **NON-READ**: creating or overwriting local files counts even when the service only returns data. Uploads and cloud-to-cloud copies also write. |
| `gcloud storage rsync ... --delete-unmatched-destination-objects` | **NON-READ**, **DESTRUCTIVE**: may overwrite and delete at the destination. A verified `--dry-run` is a separate preview. See [rsync](https://docs.cloud.google.com/sdk/gcloud/reference/storage/rsync). |
| `bq query`, even with a `SELECT` statement | **NON-READ** when executing a query job; inspect SQL, destination, billing scope, and possible external calls. A verified `--dry_run` validates/estimates without executing the query; it never authorises the real job. See [queries and dry runs](https://docs.cloud.google.com/bigquery/docs/running-queries#dry-run). |
| `gcloud auth login`, ADC login, configuration changes, API enablement | **NON-READ**: authentication, local configuration or service state changes need a plan. See [auth login](https://docs.cloud.google.com/sdk/gcloud/reference/auth/login). |
| Workload invocation, builds, deployments, SSH/SCP, job starts | **NON-READ** when they execute code, start work, transfer files, or change configuration. `--quiet` suppresses prompts; it is not a dry run or authorisation. |
