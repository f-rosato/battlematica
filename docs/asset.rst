The asset archive
=================

2D assets are neatly packaged in a structured .zip archive. The structure of the archive is showcased below with the included `default_assets.zip`. You can pass an archive with the same structure, but different files, in order to customize the graphics.


.. literalinclude:: ../structure.txt
  :language: text


Notice that the file base names end with numbers: you are free to choose the name, but the number at the end is important.
For bodies, bullets and blasts, it's what is referenced by the keys `body_type`, `bullet_type` and `blast_type` in :ref:`graphics bot settings` inside the :ref:`Write a bot file` page.
For drop ports and artifacts, the number is used according to the team they belong to (cfr. :ref:`Artifacts and drop ports`) coherently with the subfolders `team_1`, `team_2`... inside `bots`. Therefore, it's advisable that the items are color-coded coherently across the archive. If the drop port or the artifact are neutral, the file with base name ending with `0` is used.
In the background folder, you will notice the `size.txt` file: this file consists of one line with one integer, which is the side (in pixels) of the square that will tile the background filled with copies of the `.png` file in the same folder.