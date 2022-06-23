
Efter af git subtrees er på plads, og også `meta-raspberrypi`

    cd poky
    source oe-init-build-env rpi-build

Her efter har jeg tilføjet `/home/smag/workshop/poky2/poky/meta-raspberrypi \` til `poky/rpi-build/conf/bblayers.conf`.

I `poky/rpi-build/conf/local.conf` har jeg justeret lidt (caching mv), og valgt `MACHINE ?= "raspberrypi4"`

## Byg

    bitbake core-image-base

Det tager _lang_ tid. Første gang ca 6,5 time, følgende ændringer meget hurtigere, pga. cacheing.


Evt skal man køre 

    source oe-init-build-env rpi-build

igen, hvis man har lukket terminalen eller genstartet eller noget...