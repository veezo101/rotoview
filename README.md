
# Rotoview
Modding tool for the fangame, Pokemon Mystery Universe. Features a GUI built with tkinter.
It performs simple file replacements with common Python libraries.

## Features
Check out [this](https://www.youtube.com/watch?v=ygGPIg310BU&list=PLfWszzdLIYzkFRJujJusHGLTQFE7I8Rdp&index=1) short playlist showcasing features from version 0.2.5
- Auto detect path of game when running (for one time config)
- Swap & Restore Rotom sprite file to view any desired sprite available. Specfically Rotom to easily view forms. (Requires Re-opening client to view changes)
- Hot swap to and from "Silent SFX Client" while retaining any custom SFX in the unmuted mode.


Todo:
- Details of which packages to pip install etc
- Screenshots/Video demons
- Make the --add-data installation flag actually pick assets and path
- Make use of the drag and drop library added as additional hook
- Get list of pokemon with Forms using PokeAPI instead of link


## Installation

Check out [releases]() for pre-compiled versions.
If you wish to compile yourself, run the following command in the project directory with [pyinstaller](https://pypi.org/project/pyinstaller/)

```bash
pyinstaller --noconsole --onefile -n rotoview --add-data "path.txt;." --additional-hooks-dir=. --icon=rotoview.ico main.py
```
For any future installs with same settings, one can pass the created spec file to pysintaller
```bash
pyinstaller rotoview.spec
```

Once completed, a build/ and dist/ directory will be created.\
The exe can be found in the dist/ directory.\
Make sure to move over all files such as assets/ path.txt and the icon to the dist folder, in case the pyinstaller fails to do so (to be fixed later)\
Now the rotoview exe is ready to be used