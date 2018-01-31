#!/usr/bin/env bash

set -o errtrace -o nounset -o pipefail -o errexit

# Goto directory of this script
cd "$(dirname "${BASH_SOURCE[0]}")"

self_check () {
  echo "############################################"
  echo "#                                          #"
  echo "#        Self-check                        #"
  echo "#                                          #"
  echo "############################################"
  # Don't fail here, failing later at the end when all shell scripts are checked anyway.
  shellcheck ./ci.sh && echo "Self-check succeeded!" || echo "Self-check failed!"
}

setup () {
  echo "############################################"
  echo "#                                          #"
  echo "#        Environment setup                 #"
  echo "#                                          #"
  echo "############################################"
  conda info -a || true
  pip list --format=columns
}

unit_tests () {
  echo "############################################"
  echo "#                                          #"
  echo "#        Unit testing                      #"
  echo "#                                          #"
  echo "############################################"
  python setup.py test
}

beautyci () {
  echo "############################################"
  echo "#                                          #"
  echo "#        Beautysh                          #"
  echo "#                                          #"
  echo "############################################"
  pip install beautysh
  beautysh --indent-size 2 --files ci.sh
}

shell_check () {
  echo "############################################"
  echo "#                                          #"
  echo "#        Shellcheck                        #"
  echo "#                                          #"
  echo "############################################"
  find . -name "*.sh" -print0 | xargs -n 1 -0 shellcheck
}

create_source_distribution() {
  echo "############################################"
  echo "#                                          #"
  echo "#        Creating a Source Distribution    #"
  echo "#                                          #"
  echo "############################################"
  python setup.py sdist
}

check_for_clean_worktree() {
  echo "############################################"
  echo "#                                          #"
  echo "#        Check for clean worktree          #"
  echo "#                                          #"
  echo "############################################"
  # To be executed after all other steps, to ensures that there is no
  # uncommitted code and there are no untracked files, which means .gitignore is
  # complete and all code is part of a reviewable commit.
  GIT_STATUS="$(git status --porcelain)"
  if [[ $GIT_STATUS ]]; then
    echo "Your worktree is not clean, there is either uncommitted code or there are untracked files:"
    echo "${GIT_STATUS}"
    exit 1
  fi
}

self_check
setup
unit_tests
beautyci
shell_check
check_for_clean_worktree
create_source_distribution
check_for_clean_worktree
