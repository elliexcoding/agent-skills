# Examples that defeat name-based checks

These examples illustrate effects, not a complete allow-list. Recheck the exact
command, parameters, credential path, and surrounding shell before use.

| Command or pattern | Classification and reason |
| --- | --- |
| `aws ec2 describe-instances`, `aws s3api list-objects-v2` | `READ` when limited to inspection with verified context and no surrounding writes. |
| `aws sqs receive-message` | **NON-READ**: receiving affects message visibility and processing state; it is not a passive peek. See [AWS receive-message](https://docs.aws.amazon.com/cli/latest/reference/sqs/receive-message.html). |
| `aws s3api get-object ... output.bin`, S3 downloads, `... > file`, `... \| tee file` | **NON-READ**: local creation/overwrite counts even when the AWS API reads data. See [AWS get-object](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-object.html). |
| `aws s3 sync ... --delete` | **NON-READ**, **DESTRUCTIVE**: may copy, overwrite, and delete destination files/objects. A verified `--dryrun` is a separate preview, never approval for the real command. See [AWS sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html). |
| `aws cloudformation deploy ... --no-execute-changeset` | **NON-READ**: still creates a change set. See [AWS deploy](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/deploy.html). |
| `aws lambda invoke`, remote execution, job/query starts | **NON-READ** when they execute work, create jobs/results, or write files. A Lambda `DryRun` requires separate review, including its output destination. See [AWS invoke](https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html). |
| `aws sso login`, credential/configuration changes | **NON-READ**: authentication/session and local configuration/cache effects must be planned. See [AWS login](https://docs.aws.amazon.com/cli/latest/reference/sso/login.html). |
