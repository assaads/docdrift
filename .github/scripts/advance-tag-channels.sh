#!/usr/bin/env bash
# .github/scripts/advance-tag-channels.sh — move vMAJOR and vMAJOR.MINOR channel
# tags to the commit pointed at by a just-created vX.Y.Z release tag.
#
# WHY: release-please only creates exact vX.Y.Z tags. Moving channel tags
# (v0, v0.1) are a release-channel convention that consumers pin to ("latest
# 0.1.x"). They must be advanced on EVERY release or pinned consumers silently
# never update. Automating it removes the manual step that's easy to forget.
#
# Called by .github/workflows/tag-channels.yml on the `create` event for a tag.
#
# Usage: advance-tag-channels.sh <new-version-tag>   e.g. v0.1.0
#
# Exit codes: 0 = all applicable channels updated/verified; 1 = bad input;
#             2 = target tag missing.
set -euo pipefail

log() { printf '[channels] %s\n' "$*" >&2; }

TAG="${1:-}"
if [ -z "$TAG" ]; then
  log "ERROR: no version tag argument"; exit 1
fi

# Accept only vX.Y.Z (final releases — reject pre-releases and moving tags).
if ! printf '%s' "$TAG" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$'; then
  log "skip: '$TAG' is not a final vX.Y.Z tag (pre-release or channel tag)"
  exit 0
fi

# Commit the release tag points at.
if ! TARGET_SHA="$(git rev-list -n1 "$TAG" 2>/dev/null)"; then
  log "ERROR: tag '$TAG' not found in this checkout"; exit 2
fi
log "release tag $TAG -> $TARGET_SHA"

MAJOR="${TAG%%.*}"                                  # v0
REST="${TAG#*.}"                                    # 1.0
MINOR="${MAJOR}.${REST%%.*}"                        # v0.1
CHANNELS=("$MAJOR" "$MINOR")

moved=0
for ch in "${CHANNELS[@]}"; do
  cur=""
  if git rev-parse --verify --quiet "refs/tags/$ch" >/dev/null; then
    cur="$(git rev-list -n1 "$ch")"
  fi
  if [ "$cur" = "$TARGET_SHA" ]; then
    log "$ch already at $TARGET_SHA — no-op"
    continue
  fi
  # Force-move the channel ref to the release commit. -f because moving tags
  # always rewrites the ref even when the new commit is a descendant.
  git tag -f "$ch" "$TARGET_SHA" >/dev/null
  git push -f origin "refs/tags/$ch" >/dev/null
  log "$ch: ${cur:-<new>} -> $TARGET_SHA  (pushed)"
  moved=$((moved + 1))
done

log "done: $moved channel tag(s) advanced."
