# Display Lammps Log
Display the lammps log file alongside you structure data in OVITO Pr

## Description
This modifier takes in a lammps log file and adds them to the data inspector in OVITO Pro. The full thermodynamic output from lammps is available as a data table. Moreover, if thermo output has been written at the timestep currently displayed in OVITO this data will be loaded into attributes as well. Both the data table and the attributes are named as `"lammps log {key}"` where `key` is a [lammps thermo keyword](https://docs.lammps.org/thermo_style.html) found in the log file. 

## Parameters 
- `file_name` / "Lammps log file": File system path to the lammps log file.
- `group_components` / "Group components": Group components of a single thermo keyword into a single data table in OVITO. For example: Pxx, Pyy, Pzz thermo values written by lammps are packed into a single `"lammps log P"` OVITO table.
- `per_atom_energies` / "Per-atom energies": Normalize energies extracted from the lammps log by the number of particles in the system. 

## Example
<!-- ![Example 01](examples/example_01.png) -->

## Installation
- OVITO Pro [integrated Python interpreter](https://docs.ovito.org/python/introduction/installation.html#ovito-pro-integrated-interpreter):
  ```
  ovitos -m pip install --user git+https://github.com/nnn911/DisplayLammpsLog.git
  ``` 
  The `--user` option is recommended and [installs the package in the user's site directory](https://pip.pypa.io/en/stable/user_guide/#user-installs).

- Other Python interpreters or Conda environments:
  ```
  pip install git+https://github.com/nnn911/DisplayLammpsLog.git
  ```

## Technical information / dependencies
- Tested on OVITO version 3.9.2

## Contact
Daniel Utt utt@ovito.org