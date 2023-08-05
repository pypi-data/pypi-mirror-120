# adrians-geotools
Adrians-geotools is a package of three python tools originally developed by Adrian Lundell for NVI Inc. during an internship over the summer 2021.
It contains the three tools 

- EopTool, for comparing residuals between different earth orientation parameter measurments. Handles .eob, .eop .fil and .txt formats.
- HelmertTool, for transforming between different terrestial reference frames. Handles .sta formats.
- IcrfTool, for transformig between different celestial reference frames. Handles .src formats.

For any questions please email the author at adrian.lundell@gmail.com.

## Installation 
The package is installable using PyPi through

```bash
pip install adrians-geotools
```

or by downloading the source code from github and installing the requirements

```bash
git clone https://github.com/AdrianLundell/adrians-geotools.git
pip install -r adrians-geotools/requirements.txt
```

Installation is generally recommended within a seperate virtual environment to avoid version dependency problems, please see https://docs.python.org/3/tutorial/venv.html for more information.


## Usage 
If the project was installed with PyPip the tool interfaces may be run directly in a terminal using their respective names. 

```bash
EopTool
HelmertTool
IcrfTool
```

Otherwise, run them as modules using

```bash
python -m EopTool
python -m HelmertTool
python -m IcrfTool
```

assuming adrian-geotools to be your working directory. 

To use the tools in your own python scripts simply import them as with any other library, e.g.

Example files are runneable only with the pypi installation, or by moving the files.

```python
from HelmertTool.calc import calculate_parameters
import EopTool  
```

## Contributing 

The package is currently not under development but please submit issues to the github page for future improvements.

## License 

See license. The map.png file used in HelmertTool is generated with the geopandas library, please see https://geopandas.org/about.html
