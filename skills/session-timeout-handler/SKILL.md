---
name: session-timeout-handler
description: "Build timeout-resistant Claude Code workflows using chunking, checkpoints, and resume patterns to handle 2-minute tool timeouts. Use when a task keeps timing out, an operation runs too long, you need to break up large tasks, or you encounter timeout errors during bulk processing, builds, or API calls."
license: MIT
tags: [timeout, resilience, workflow, chunking, checkpoints, claude-code]
---

# Session Timeout Handler

Build resilient workflows that gracefully handle Claude Code's 2-minute timeout constraints through intelligent chunking, checkpoints, and resumability.

## Core Patterns

### 1. Batch Processing

Split large item lists into small batches that complete well within the timeout window.

```bash
#!/bin/bash
# Process items in small batches with resume support

ITEMS_FILE="items.txt"
BATCH_SIZE=10
OFFSET=${1:-0}

tail -n +$((OFFSET + 1)) "$ITEMS_FILE" | head -$BATCH_SIZE | while read item; do
    process_item "$item"
    echo "Processed: $item"
done

NEXT_OFFSET=$((OFFSET + BATCH_SIZE))
TOTAL=$(wc -l < "$ITEMS_FILE")

if [ $NEXT_OFFSET -lt $TOTAL ]; then
    echo "Progress: $NEXT_OFFSET/$TOTAL — Run: ./script.sh $NEXT_OFFSET"
else
    echo "All items processed!"
fi
```

### 2. Checkpoint Resume

Persist progress after each item so work survives interruptions and resumes automatically.

```bash
#!/bin/bash
# Checkpoint-based workflow — survives interruptions

CHECKPOINT_FILE=".progress"
ITEMS=("item1" "item2" "item3" "item4" "item5")  # Your item list
BATCH_SIZE=10

LAST_COMPLETED=$(cat "$CHECKPOINT_FILE" 2>/dev/null || echo "-1")
START=$((LAST_COMPLETED + 1))
END=$((START + BATCH_SIZE))
[ $END -gt ${#ITEMS[@]} ] && END=${#ITEMS[@]}

for i in $(seq $START $((END - 1))); do
    process "${ITEMS[$i]}"
    echo "$i" > "$CHECKPOINT_FILE"  # Save after each item
    echo "Completed $((i + 1))/${#ITEMS[@]}"
done

if [ $END -ge ${#ITEMS[@]} ]; then
    echo "All items complete!"
    rm "$CHECKPOINT_FILE"
else
    echo "Run again to continue from item $END"
fi
```

### 3. State Machine

Decompose multi-phase workflows into discrete states, advancing one phase per invocation.

```bash
#!/bin/bash
# Multi-phase state machine — one phase per run

STATE_FILE=".workflow_state"
STATE=$(cat "$STATE_FILE" 2>/dev/null || echo "INIT")

advance_state() { echo "$1" > "$STATE_FILE"; echo "Phase complete. Run again for next phase."; }

case $STATE in
    INIT)       setup_environment;   advance_state "DOWNLOAD" ;;
    DOWNLOAD)   download_resources;  advance_state "PROCESS"  ;;
    PROCESS)    process_data;        advance_state "FINALIZE" ;;
    FINALIZE)   cleanup_and_report;  echo "COMPLETE" > "$STATE_FILE"; echo "Workflow complete!" ;;
    COMPLETE)   echo "Already completed."; cat results.txt ;;
esac
```

## Timeout-Safe Techniques

### Timeout with Fallback

Wrap individual operations with a timeout shorter than the 2-minute limit, falling back to cached results on failure.

```bash
#!/bin/bash
OPERATION_TIMEOUT=90  # Leave buffer below 120s limit

if timeout ${OPERATION_TIMEOUT}s expensive_operation > result.txt 2>&1; then
    echo "Operation completed"
    cat result.txt
elif [ $? -eq 124 ]; then
    echo "Timed out after ${OPERATION_TIMEOUT}s"
    # Fall back to cached result or partial output
    [ -f "cached_result.txt" ] && cat cached_result.txt || cat result.txt
    echo "Run again to continue processing"
else
    echo "Operation failed"
fi
```

### Parallel with Rate Limiting

Run multiple items concurrently while staying within resource limits.

```bash
#!/bin/bash
MAX_PARALLEL=3

for item in $(seq 1 15); do
    # Cap concurrent jobs
    while [ $(jobs -r | wc -l) -ge $MAX_PARALLEL ]; do wait -n; done

    ( process_item "item-$item" && echo "Done: item-$item" ) &
    sleep 0.5  # Rate limiting
done

wait
echo "All processing complete"
```

### Progress Tracking

Track detailed progress in a JSON file for visibility and resume support.

```bash
#!/bin/bash
PROGRESS_FILE="progress.json"

# Initialize: echo '{"total":100,"completed":0,"failed":0}' > "$PROGRESS_FILE"

# Update after each item:
jq --arg item "$1" --arg status "$2" \
   '.completed += (if $status == "success" then 1 else 0 end) |
    .failed += (if $status == "failed" then 1 else 0 end)' \
   "$PROGRESS_FILE" > "$PROGRESS_FILE.tmp" && mv "$PROGRESS_FILE.tmp" "$PROGRESS_FILE"

# Show progress:
jq -r '"Progress: \(.completed)/\(.total) completed, \(.failed) failed"' "$PROGRESS_FILE"
```

## Best Practices

**Do:**
- Chunk operations into 5-10 item batches
- Save checkpoints after each item or batch
- Set individual operation timeouts to 60-90s (buffer below 120s)
- Report progress clearly so the next turn knows where to resume
- Clean up checkpoint files when workflow completes

**Avoid:**
- Processing 50+ items in a single run
- Skipping checkpoints on long workflows
- Ignoring timeout exit codes (handle exit code 124)
- Running more than 3-5 concurrent background jobs
- Retrying failed items indefinitely (limit to 3 attempts)

## Quick Reference

```bash
# Batch processing
tail -n +$OFFSET file.txt | head -$BATCH_SIZE | while read item; do process; done

# Checkpoint resume
LAST=$(cat .checkpoint || echo 0); process_from $LAST

# State machine
case $(cat .state) in PHASE1) step1 ;; PHASE2) step2 ;; esac

# Progress display
echo "Progress: $COMPLETED/$TOTAL ($((COMPLETED * 100 / TOTAL))%)"

# Timeout with fallback
timeout 90s operation || use_cached_result

# Parallel with limit
for i in items; do process &; [ $(jobs -r | wc -l) -ge $MAX ] && wait -n; done
```

See [EXAMPLES.md](./EXAMPLES.md) for complete real-world examples including bulk repository cloning, large dataset processing, API scraping with rate limits, and multi-turn Claude Code workflows.
