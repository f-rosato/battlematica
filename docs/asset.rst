The asset archive
=================

2D assets are neatly packaged in a structured .zip archive. The structure of the archive is
showcased below with the included `default_assets.zip`. You can pass an archive with the same
structure, but different files, in order to customize the graphics. :

.. code-block:: text

    |
    +---artifacts
    |       artifact0.png
    |       artifact1.png
    |       artifact2.png
    |       artifact3.png
    |
    +---background
    |       background_1.png
    |       size.txt
    |
    +---blasts
    |       blast01.png
    |       blast02.png
    |       blast03.png
    |       blast04.png
    |
    +---bots
    |   +---team_1
    |   |       enemyBlue1.png
    |   |       enemyBlue2.png
    |   |       enemyBlue3.png
    |   |       enemyBlue4.png
    |   |       enemyBlue5.png
    |   |
    |   +---team_2
    |   |       enemyRed1.png
    |   |       enemyRed2.png
    |   |       enemyRed3.png
    |   |       enemyRed4.png
    |   |       enemyRed5.png
    |   |
    |   \---team_3
    |           enemyGreen1.png
    |           enemyGreen2.png
    |           enemyGreen3.png
    |           enemyGreen4.png
    |           enemyGreen5.png
    |
    +---bullets
    |       laserBlue01.png
    |       laserBlue02.png
    |       laserBlue03.png
    |       laserBlue04.png
    |       laserBlue05.png
    |       laserBlue06.png
    |       laserBlue07.png
    |       laserBlue08.png
    |       laserBlue09.png
    |       laserBlue10.png
    |       laserBlue11.png
    |       laserBlue12.png
    |
    \---drop_ports
            dp0.png
            dp1.png
            dp2.png
            dp3.png


Notice that the file base names end with numbers: you are free to choose the name, but the number at the end is
important.

For bodies, bullets and blasts, it's what is referenced by the keys `body_type`, `bullet_type` and `blast_type` in :ref:`graphics bot settings`
inside the :ref:`Write a bot file` page.

For drop ports and artifacts, the number is used according to the team they belong to (cfr. :ref:`Artifacts and drop ports`)
coherently with the subfolders `team_1`, `team_2`... inside `bots`. Therefore,
it's advisable that the items are color-coded coherently across the archive. If the drop port or the
artifact are neutral, the file with base name ending with `0` is used.

In the background folder, you will notice the `size.txt` file: this file consists of one line with
one integer, which is the side (in pixels) of the square that will tile the background filled with copies
of the `.png` file in the same folder.