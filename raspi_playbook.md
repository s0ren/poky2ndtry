
Efter af git subtrees er på plads, og også `meta-raspberrypi`

    cd poky
    source oe-init-build-env rpi-build

Her efter har jeg tilføjet `/home/smag/workshop/poky2/poky/meta-raspberrypi \` til `poky/rpi-build/conf/bblayers.conf`.

I `poky/rpi-build/conf/local.conf` har jeg justeret lidt (caching mv), og valgt `MACHINE ?= "raspberrypi4"`

## Byg

    cd rpi-build
    bitbake core-image-base

Det tager _lang_ tid. Første gang ca 6,5 time, følgende ændringer meget hurtigere, pga. cacheing.


Evt skal man køre 

    source oe-init-build-env rpi-build

igen, hvis man har lukket terminalen eller genstartet eller noget...

Når `bitbake` er færdig, ligger der noget i mappen `poky/rpi-build/tmp/deploy/images/raspberrypi4`

    ls -l tmp/deploy/images/raspberrypi4/*.bz2

[out]:

    -rw-r--r-- 2 smag smag 42295779 jun 23 16:30 tmp/deploy/images/raspberrypi4/core-image-base-raspberrypi4-20220623133557.rootfs.tar.bz2
    -rw-r--r-- 2 smag smag 63144306 jun 23 16:30 tmp/deploy/images/raspberrypi4/core-image-base-raspberrypi4-20220623133557.rootfs.wic.bz2
    lrwxrwxrwx 2 smag smag       58 jun 23 16:30 tmp/deploy/images/raspberrypi4/core-image-base-raspberrypi4.tar.bz2 -> core-image-base-raspberrypi4-20220623133557.rootfs.tar.bz2
    lrwxrwxrwx 2 smag smag       58 jun 23 16:31 tmp/deploy/images/raspberrypi4/core-image-base-raspberrypi4.wic.bz2 -> core-image-base-raspberrypi4-20220623133557.rootfs.wic.bz2

Det er `core-image-base-raspberrypi4-20220623133557.rootfs.wic.bz2` som er image filen. Sym-linket `core-image-base-raspberrypi4.wic.bz2` er for at man ikke skal have besvær med tidstemplet i filnavnet.

Man kan kopiere image'et med `bmaptool`.

Den skal istalleres med:

    sudo apt install bmap-tools

Vi vil også gerne vide hvor sdkort læser/skriveren er placeret, derfor kører vi lige programmet `lsblk`:

    lsblk

[out]:

    NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    loop0    7:0    0     4K  1 loop /snap/bare/5
    loop1    7:1    0  61,9M  1 loop /snap/core20/1328
    loop2    7:2    0  65,2M  1 loop /snap/gtk-common-themes/1519
    loop3    7:3    0 248,8M  1 loop /snap/gnome-3-38-2004/99
    loop4    7:4    0 220,5M  1 loop /snap/code/99
    loop5    7:5    0 113,9M  1 loop /snap/core/13308
    loop6    7:6    0  61,9M  1 loop /snap/core20/1518
    loop7    7:7    0  43,6M  1 loop /snap/snapd/14978
    loop8    7:8    0 254,1M  1 loop /snap/gnome-3-38-2004/106
    loop9    7:9    0  54,2M  1 loop /snap/snap-store/558
    loop10   7:10   0    47M  1 loop /snap/snapd/16010
    loop11   7:11   0  81,3M  1 loop /snap/gtk-common-themes/1534
    sda      8:0    0 465,8G  0 disk 
    ├─sda1   8:1    0   512M  0 part /boot/efi
    ├─sda2   8:2    0     1K  0 part 
    └─sda5   8:5    0 465,3G  0 part /
    sdb      8:16   1  29,7G  0 disk 
    ├─sdb1   8:17   1  50,3M  0 part /media/smag/boot
    └─sdb2   8:18   1 140,4M  0 part /media/smag/root
    sr0     11:0    1  1024M  0 rom  

Man kan se at sd-kortet er på `sdb`, fordi størrelsen passer ca med et 32GB kort. `sda` er nok laptoppens hardisk, med 465GB.

Hvis der er mountet noget fra sdkortet, skal det lige unmountes:

    sudo umount /media/smag/boot 
    sudo umount /media/smag/root 

Nu:

    sudo bmaptool copy tmp/deploy/images/raspberrypi4/core-image-base-raspberrypi4.wic.bz2 /dev/sdb
    
[out]:

    bmaptool: info: discovered bmap file 'tmp/deploy/images/raspberrypi4/core-image-base-raspberrypi4.wic.bmap'
    bmaptool: info: block map format version 2.0
    bmaptool: info: 51610 blocks of size 4096 (201.6 MiB), mapped 27982 blocks (109.3 MiB or 54.2%)
    bmaptool: info: copying image 'core-image-base-raspberrypi4.wic.bz2' to block device '/dev/sdb' using bmap file 'core-image-base-raspberrypi4.wic.bmap'
    bmaptool: info: 100% copied
    bmaptool: info: synchronizing '/dev/sdb'
    bmaptool: info: copying time: 11.6s, copying speed 9.4 MiB/sec

