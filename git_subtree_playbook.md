# Playbook for at lægge poky mv ind som subtrees

## Opstart

Opstarten kan muligvis springes over. Se ... [overskrift]

### Init

Først skal vi have mappen til at være et git repo. Den skal med andre or initialisers:

    git init

### Første commit

Vi laver et commit af hvad der er i mappen indtil nu...

    git add .
    git commit . -m "første commit"

[out]:

    [master (root-commit) a1c6d35] første commit
    2 files changed, 3 insertions(+)
    create mode 100644 git_subtree_p

### Ny branch

Vi skifter til ny branch og opretter den samtidigt:

    git checkout -b subtrees

[out]:

    Switched to a new branch 'subtrees'

### hent 'poky' ind som subtree


    git subtree add -P poky --squash git://git.yoctoproject.org/poky kirkstone -m "poky kirkstone hentet"

