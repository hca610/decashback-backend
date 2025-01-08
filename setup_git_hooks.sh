#!/bin/bash
CURRENT_DIR=$(pwd)

# Setup commit-msg hook
chmod +x $CURRENT_DIR/.git_hooks/commit-msg
ln -s -f $CURRENT_DIR/.git_hooks/commit-msg $CURRENT_DIR/.git/hooks/commit-msg
echo "commit-msg installed at $CURRENT_DIR/.git/hooks/commit-msg"

# Setup pre-commit hook
pre-commit install --config $CURRENT_DIR/.git_hooks/pre-commit-config.yaml
