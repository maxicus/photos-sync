# photos-sync
synchronizes converted and raw photos folders.

You may have folder with raw photos, and script will create equal folder structure with photos converted for fast view (.jpg of screen size).
Once built, folder structures are tracked and synchronized.
i.e. raw is updated -> view file regenerated.

view file is moved -> raw file is moved.
view file is deleted -> raw file is deleted.
(the same for other side).

Limiation: filenames must be unique across whole library, since it tracks by filename.
Good way to uniqualize it is by using creation date as a filename. For example can be done by:
```
exiv2 -r'%y%m%d_%H%M%S' -F rename *
```

# Installation

modify `config.py` with your paths.
Start script by executing `python main.py`

# Example:
you create files in 2 albums:
```
raw/running_home/1.crw
raw/running_home/2.crw
raw/at_work/3.crw
raw/at_work/4.crw
```
run the script `python main.py` and it creates
```
view/running_home/1.jpg
view/running_home/2.jpg
view/at_work/3.jpg
view/at_work/4.jpg
```
manually move `view/at_work/4.jpg` to `view/running_home/4.jpg`, run script and it will move `raw/at_work/4.jpg` to `raw/running_home/4.jpg`

delete view/running_home/4.jpg and it will delete raw/running_home/4.jpg (it doesnt delete files, but move them to "deleted" folder)
