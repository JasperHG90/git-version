#! /usr/bin/env bash

VERSION_PATTERN='v{0,1}[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}'

# On release, we expect a tag to be present in a correct format
#  see VERSION_PATTERN above.
TAG_CURRENT_COMMIT=$(git tag --points-at HEAD)
if [ -z "$TAG_CURRENT_COMMIT" ]; then
    # Here, we need to be careful to select the latest tag in a proper format. If another tag in a non-standard format is present, we should ignore it.
    #  because users may use tags for other purposes than versioning.
    LATEST_TAG=$(git tag --points-at $(git rev-list --tags --grep $VERSION_PATTERN --max-count=1)) # NB: ignore warning if no tags are present
    # No tag present
    if [ -z "$LATEST_TAG" ]; then
        LATEST_TAG_PARSED="0.0.0"
        # Get fist commit ever
        LATEST_TAG_COMMIT_SHA=$(git rev-list --max-parents=0 HEAD)
    else
        if [[ $LATEST_TAG =~ $VERSION_PATTERN ]]; then
            LATEST_TAG_PARSED="${BASH_REMATCH[0]}"
        fi
        LATEST_TAG_COMMIT_SHA=$(git rev-list -n 1 $LATEST_TAG)
    fi
    DISTANCE="a$(git rev-list --count $LATEST_TAG_COMMIT_SHA..HEAD)"
    CURRENT_COMMIT_SHA_SHORT=$(git rev-parse --short HEAD)
    # Remove 'v' if present
    echo "${LATEST_TAG_PARSED//v}$DISTANCE+$CURRENT_COMMIT_SHA_SHORT"
else
    # If released with inappropriate tag, then fail with warning
    if [[ $TAG_CURRENT_COMMIT =~ $VERSION_PATTERN ]]; then
        TAG_CURRENT_COMMIT_PARSED="${BASH_REMATCH[0]//v}"
    else
        echo "Tag '$TAG_CURRENT_COMMIT' is not in the correct format. Please use the format '(v)MAJOR.MINOR.PATCH', e.g. 'v1.0.0'"
        exit 1
    fi    
    echo "$TAG_CURRENT_COMMIT_PARSED"
fi
