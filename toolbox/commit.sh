#!/bin/bash
# This script modifies sandbox files so that package-diff can be executed with mocked Pipfile changes.

pushd "$(dirname "$(cd "$(dirname "$0")" && pwd)")" > /dev/null || exit 1

printf "\e[33m\nWarning: This script should only be used for testing commit template rendering.\e[0m "
echo "$@" | grep --quiet "\-\-no\-edit"
EXIT_CODE=$?
if [ "$EXIT_CODE" -ne 0 ]; then
    printf "\e[33mAbort or manually cleanup the following commit (ye be warned).\e[0m\n\n"
else
    printf "\e[33mPassing --no-edit will create a commit that needs to be manually cleaned up (ye be warned).\e[0m\n\n"
fi
read -n 1 -s -r -p "Press any key to continue..."

PIPFILE=toolbox/sandbox/Pipfile
if [ ! -f "$PIPFILE" ]; then
    printf "\e[31mError: %s does not exist\e[0m\n" $PIPFILE
    exit 1
fi

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

pipenv run package-diff commit $PIPFILE "$@"

pipfiles=("$PIPFILE" "$PIPFILE_LOCK")
for P in "${pipfiles[@]}"; do
    git reset --quiet -- "$P"
    EXIT_CODE=$?
    if [ "$EXIT_CODE" -ne 0 ]; then
        printf "\e[31mError: Failed to unstage %s\e[0m\n" "$P"
        exit $EXIT_CODE
    fi

    git checkout -- "$P"
    EXIT_CODE=$?
    if [ "$EXIT_CODE" -ne 0 ]; then
        printf "\e[31mError: Failed to revert changes to %s\e[0m\n" "$P"
        exit $EXIT_CODE
    fi
done
