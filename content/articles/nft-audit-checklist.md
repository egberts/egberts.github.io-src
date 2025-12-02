title: Netfilter/nftables Audit Checklist
date: 2025-08-20 07:05
status: published
tags: netfilter, nftables, nft, audit, security
category: research
summary: A checklist for auditing nftables ruleset
slug:
lang: en
private: False

`nftables` Best Practices Checklist

## 1. Chain & Rule Definition
- [ ] Base chains explicitly defined with correct `type`, `hook`, and `priority`.
- [ ] Non-base (regular) chains used for modularity and clarity.
- [ ] Use `jump` vs. `goto` correctly based on control flow needs.
- [ ] Include `return` where appropriate in regular chains.
- [ ] Avoid overly complex or deeply nested chain calls.

## 2. Naming & Documentation
- [ ] Use descriptive and consistent naming conventions for tables, chains, sets, and rules.
- [ ] Add comments explaining the purpose and logic of chains and critical rules.
- [ ] Avoid generic or ambiguous names like `chain1`, `temp`, or `debug` without context.

## 3. Rule Order & Policies
- [ ] Rules within chains ordered logically — specific matches before general ones.
- [ ] Catch-all policies (accept/drop) placed at the end of chains.
- [ ] Default policies set deliberately on base chains (`accept` or `drop`).

## 4. Logging & Monitoring
- [ ] Logging is used sparingly and only where necessary.
- [ ] Log prefixes clearly identify the source chain/rule.
- [ ] Logs are forwarded to secure and monitored locations.
- [ ] Monitor logs for unusual or unexpected activity.

## 5. Sets & Maps
- [ ] Use sets/maps for efficient matching where applicable.
- [ ] Update sets atomically or during maintenance windows.
- [ ] Document dynamic updates to sets/maps.

## 6. Configuration Management
- [ ] Use version control (e.g., Git) for nftables configs.
- [ ] Require reviews and approvals for changes.
- [ ] Ensure ruleset persistence across reboots.
- [ ] Backup configs before making changes.

## 7. Auditing & Testing
- [ ] Regularly audit for:
  - Unused or orphaned chains
  - Unexpected jumps/gotos
  - Changes in policies or logging
- [ ] Test new rules in staging environments.
- [ ] Automate ruleset validation and alerts on suspicious changes.

## 8. Performance & Stability
- [ ] Avoid excessive logging in high-traffic paths.
- [ ] Limit rule complexity to maintain performance.
- [ ] Monitor firewall resource usage.

---

# nftables Audit Script Ideas

## 1. List All Chains & Their Types

```bash
#!/bin/bash
echo "Listing all tables and their chains with type, hook, priority, and policy:"
nft list tables | while read -r line; do
  family=$(echo "$line" | awk '{print $2}')
  table=$(echo "$line" | awk '{print $3}')
  echo "Table: $table (family $family)"

  sudo /opt/nftables/sbin/nft list table "$family" "$table" | awk -v table="$table" '
    function print_chain() {
      if (chain != "") {
        if (is_base)
          print "[BASE]     " chain (pol == "" ? "\n⚠  WARNING: Base chain \x27" cname "\x27 missing policy!" : "")
        else
          print "[NON-BASE] " chain
      }
    }

    /^\s*chain/ {
      print_chain()  # Print previous chain before starting a new one
      chain = "Chain: " $2
      cname = $2
      is_base = 0
      pol = ""
      type = hook = prio = ""  # Reset values for clarity
    }

    /type/ {
      for (i = 1; i <= NF; i++) {
        if ($i == "type")     type = $(i + 1)
        if ($i == "hook")     hook = $(i + 1)
        if ($i == "priority") prio = $(i + 1)
        if ($i == "policy")   pol  = $(i + 1)
      }
      chain = chain " | type: " type " | hook: " hook " | priority: " prio " | policy: " pol
      is_base = 1
    }

    END {
      print_chain()  # Print the final chain!
    }
  '

  echo
done
```


2. Find All Jump & Goto Targets

```bash
#!/bin/bash
echo "Jump and Goto usage in ruleset:"
nft list ruleset | grep -E 'jump|goto' | awk '{print NR, $0}'
```

3. Detect Unused Chains

```bash
#!/bin/bash
# List all chain names
chains=$(nft list chains | awk '{print $2}')

# List all chains referenced in jump/goto
refs=$(nft list ruleset | grep -Eo 'jump [^ ]+|goto [^ ]+' | awk '{print $2}' | sort | uniq)

echo "Chains defined but never jumped/goto'd:"
for chain in $chains; do
  if ! grep -qw "$chain" <<< "$refs"; then
    echo " - $chain"
  fi
done
```

4. Extract Chains Without Return

```bash
#!/bin/bash
echo "🔎 Scanning for non-base chains *without* a 'return' statement..."

current_family=""
current_table=""
in_chain=0
chain_name=""
has_hook=0

nft list ruleset | while IFS= read -r line; do
  # Track family and table
  if [[ $line =~ ^table[[:space:]]+([a-z0-9]+)[[:space:]]+([a-zA-Z0-9_]+)[[:space:]]*{ ]]; then
    current_family="${BASH_REMATCH[1]}"
    current_table="${BASH_REMATCH[2]}"
  fi

  # Detect start of a chain block
  if [[ $line =~ ^[[:space:]]*chain[[:space:]]+([a-zA-Z0-9_]+)[[:space:]]*{ ]]; then
    chain_name="${BASH_REMATCH[1]}"
    in_chain=1
    has_hook=0
    continue
  fi

  # Look for hook line inside chain
  if [[ $in_chain -eq 1 && $line =~ hook ]]; then
    has_hook=1
  fi

  # Detect end of chain block
  if [[ $in_chain -eq 1 && $line =~ ^[[:space:]]*} ]]; then
    if [[ $has_hook -eq 0 ]]; then
      # Non-base chain — test if it lacks 'return'
      if ! nft list chain "$current_family" "$current_table" "$chain_name" 2>/dev/null | grep -q '\breturn\b'; then
        echo " - $current_family $current_table $chain_name"
      fi
    fi
    in_chain=0
    chain_name=""
  fi
done
```
Adjust the table/family name (inet filter) accordingly.

5. Verify Default Policies

```bash
#!/bin/bash
echo "Base chains and their policies (if any):"
nft list tables | while read -r table_full; do
  table="${table_full#table }"
  echo "Table: $table"
  
  nft list "$table_full" 2>/dev/null | grep -E '^\s*chain' | while read -r line; do
    chain=$(echo "$line" | awk '{print $2}')
    policy=$(echo "$line" | grep -o 'policy [a-z]*' | awk '{print $2}')
    if [ -n "$policy" ]; then
      echo " - Chain: $chain, Policy: $policy"
    else
      echo " - Chain: $chain, Policy: (none)"
    fi
  done
done
```

6. Check for Suspicious Logging

```bash
#!/bin/bash

echo "== Log rules with prefixes =="
nft list ruleset | grep 'log prefix' || echo "No log prefix rules found."

echo -e "\n== DROP or REJECT rules without logging =="
nft list ruleset | grep -E 'drop|reject' | grep -v 'log' || echo "No DROP/REJECT rules without logging found."

echo -e "\n== Rules with multiple logging actions or suspicious prefixes =="
nft list ruleset | grep -E 'log prefix' | awk '
  {
    prefix_count = gsub(/log prefix/, "log prefix");
    if (prefix_count > 1) {
      print "Rule with multiple log actions: " $0
    }
    if ($0 ~ /log prefix "[^"]{0,3}"/) {
      print "Rule with suspiciously short log prefix: " $0
    }
  }
' || echo "No suspicious logging rules found."

echo -e "\n== Rules with unusual verdicts (QUEUE, CONTINUE, etc.) =="
nft list ruleset | grep -E 'queue|continue|immediate' || echo "No unusual verdicts found."

echo -e "\n== Rules with zero packet matches (potentially dead) =="
nft list ruleset | grep 'packets 0 bytes' || echo "No rules with zero matches found."
```

Bonus: Automated Notifications

* Schedule these scripts with cron for periodic checks.
* Send results via email or integrate with monitoring systems.
* Compare current output with previous runs to detect unexpected changes.
