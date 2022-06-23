
Efter af git subtrees er på plads, og også `meta-raspberrypi`

    cd poky
    oe-init-build-env rpi-build

Her efter har jeg tilføjet `/home/smag/workshop/poky2/poky/meta-raspberrypi \` til `poky/rpi-build/conf/bblayers.conf`.

I `poky/rpi-build/conf/local.conf` har jeg justeret lidt (caching mv), og valgt `MACHINE ?= "raspberrypi4"`