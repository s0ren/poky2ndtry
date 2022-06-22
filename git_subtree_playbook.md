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


## subtrees

### hent 'poky' ind som subtree

    git subtree add -P poky --squash git://git.yoctoproject.org/poky kirkstone -m "poky kirkstone hentet"

[out]:

    git fetch git://git.yoctoproject.org/poky kirkstone
    warning: no common commits
    remote: Enumerating objects: 486569, done.
    remote: Counting objects: 100% (61213/61213), done.
    remote: Compressing objects: 100% (7967/7967), done.
    remote: Total 486569 (delta 58227), reused 53333 (delta 53245), pack-reused 425356
    Receiving objects: 100% (486569/486569), 170.84 MiB | 536.00 KiB/s, done.
    Resolving deltas: 100% (349695/349695), done.
    From git://git.yoctoproject.org/poky
    * branch                  kirkstone  -> FETCH_HEAD
    Added dir 'poky'

__note__ Man skal lige commit'e ændringer inden man kan udføre `git subtree add ...`:

    git commit . "mere ..."

### hent meta-raspberrypi som subtree til poky

I undermappen `poky` som vi lige har lavet med `git subtree add ...` skal vi have en ny undermappe med et subtree af BSP laget _`meta-rraspberrypi`_  
Man skal være i projektet rod, for at køre kommandoen.
Bemærk at det skal være branchen  _`kirkstone`_.

    git subtree add -P poky/meta-raspberrypi --squash git://git.yoctoproject.org/meta-raspberrypi kirkstone -m "meta-raspberrypi kirkstone hentet"

## Ny branch

For at holde en adskillese mellem de indhentningen af kode til subtrees, og det viddere arbejde, laver jeg et subtree, igen:

    git checkout -b first_raspi

 