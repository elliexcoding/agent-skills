# Kubernetes Review Lens

Use this lens for supplied Kubernetes manifests and rendered resources. Ask
observable failure questions; do not assume a distribution, admission setup,
or cluster policy.

Before reporting a cluster-dependent issue, identify the exact workload and
rendered resource, target cluster/version, namespace, and the relevant
admission, policy, DNS, storage, or controller assumption. Without that
evidence, record a bounded question or residual risk rather than a finding.

## Identity and isolation

- Does the workload use the intended ServiceAccount? Is token automounting
  needed, and does its RBAC grant only the verbs, resources, names, and
  namespaces the workload actually reaches? Can an allowed `create`, `bind`,
  `escalate`, impersonation, or secret read expand that authority?
  (`K8S-RBAC`)
- Is namespace membership a meaningful trust boundary in the stated cluster,
  or can shared ServiceAccounts, privileged controllers, or cross-namespace
  bindings defeat the assumed isolation? (`K8S-RBAC`)

## Pod and supply-chain security

- Do Pod and container security contexts satisfy the declared Pod Security
  level: non-root execution, non-escalation, dropped capabilities, restricted
  host namespaces/paths, and an explicit compatible seccomp profile? Can the
  image, command, mounted secret, or writable volume bypass those controls?
  (`K8S-POD-SECURITY`, `K8S-SECURITY`)
- Is each image identity immutable enough for the deployment promise, and are
  pull credentials and application secrets absent from labels, environment
  dumps, logs, and unintended mounts? (`K8S-SECURITY`)

## Selectors, traffic, and policy

- Does every controller selector match its pod-template labels, and is a
  selector change being applied to an existing object whose selector is
  immutable? Trace labels through owner relationships, Services, Ingress or
  Gateway routing, NetworkPolicies, and any monitoring or autoscaling
  selectors; which concrete pods lose or gain traffic? (`K8S-DEPLOYMENTS`)
- Do declared container ports, Service target ports, protocol assumptions,
  NetworkPolicies, and DNS names resolve to the intended workload under the
  supplied namespace and cluster configuration? Treat CNI, mesh, and DNS
  behavior as environment assumptions unless provided.

## Health and termination

- Can startup, readiness, and liveness probes distinguish slow initialization,
  temporary dependency loss, and a permanently wedged process? Does a failed
  readiness check remove traffic without creating a restart loop, and do probe
  paths, ports, auth, and timeouts exist in the rendered container? (`K8S-PROBES`)
- Is the termination grace period sufficient for in-flight work, pre-stop
  hooks, drain signaling, and volume or queue handoff? Would disruption-budget
  settings leave enough replicas available during voluntary disruption?

## Capacity, placement, and storage

- Do requests and limits support the stated workload behavior, including
  memory-pressure, CPU throttling, quota, and autoscaling signals? Are metrics
  and scaling targets actually present for the target cluster? (`K8S-RESOURCES`)
- Can node selectors, tolerations, affinity/anti-affinity, topology spread,
  priorities, and failure domains place the requested replicas during a node
  or zone loss? Do volumes have the required access mode, binding behavior,
  backup, and attachment assumptions?

## Rollout and API ownership

- For a Deployment, StatefulSet, DaemonSet, Job, or CronJob, does the update
  strategy preserve ordering, availability, data identity, retry, and rollback
  needs? Could an image/config change, partition, surge/unavailable setting,
  or schedule overlap create duplicate work or an unrecoverable rollout?
  (`K8S-DEPLOYMENTS`)
- Are CRD/API versions served by the target cluster, and are defaulted fields,
  conversion, admission mutation, GitOps ownership, and server-side-apply
  field managers compatible with this change? Report conflicts only with the
  relevant controller, ownership, or cluster evidence.
