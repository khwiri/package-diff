#!/bin/bash
# This script modifies sandbox files so that package-diff can be executed with mocked Pipfile changes.

pushd "$(dirname "$(cd "$(dirname "$0")" && pwd)")" > /dev/null || exit 1

PIPFILE_LOCK=toolbox/sandbox/Pipfile.lock
if [ ! -f "$PIPFILE_LOCK" ]; then
    printf "\e[31mError: %s does not exist\e[0m\n" $PIPFILE_LOCK
    exit 1
fi

VIEW_PIPFILE_LOCK=toolbox/sandbox/View.Pipfile.lock
if [ ! -f "$VIEW_PIPFILE_LOCK" ]; then
    printf "\e[31mError: %s does not exist\e[0m\n" $VIEW_PIPFILE_LOCK
    exit 1
fi

cp "$VIEW_PIPFILE_LOCK" "$PIPFILE_LOCK" &>/dev/null
EXIT_CODE=$?
if [ "$EXIT_CODE" -ne 0 ]; then
    printf "\e[31mError: Unable to Overwrite %s with %s\e[0m\n" $VIEW_PIPFILE_LOCK $PIPFILE_LOCK
    exit $EXIT_CODE
fi

pipenv run package-diff view toolbox/sandbox/Pipfile "$@"

git checkout -- $PIPFILE_LOCK
EXIT_CODE=$?
if [ "$EXIT_CODE" -ne 0 ]; then
    printf "\e[31mError: Failed to revert changes to %s\e[0m\n" $PIPFILE_LOCK
    exit $EXIT_CODE
fi
