#### Display Lammps Log ####
# Add thermodynamic data from lammps to OVITO

import glob
from pathlib import Path

import lmParse as lp
import numpy as np
from ovito.data import DataCollection, DataTable
from ovito.pipeline import ModifierInterface
from traits.api import Bool, Str


class DisplayLammpsLog(ModifierInterface):
    file_name = Str("", label="Lammps log file")
    group_components = Bool(False, label="Group components")
    normalize_eng = Bool(False, label="Normalize energies")

    @staticmethod
    def groupComponents(keys):
        keys_edit = list(keys)
        suffix = "Eng"
        key_groups = {suffix: []}

        # Group Energies
        for k in keys:
            if k.endswith(suffix):
                key_groups[suffix].append(k)
                keys_edit.remove(k)
        keys = keys_edit.copy()

        # Group other properties
        suffixes = (
            (
                "xx",
                "yy",
                "zz",
                "xy",
                "xz",
                "yz",
            ),
            ("x,y,z"),
        )
        for suffix in suffixes:
            keys = keys_edit.copy()
            for s in suffix:
                for k in keys:
                    if k.endswith(s):
                        prefix = k.rstrip(s)
                        if prefix not in key_groups:
                            key_groups[prefix] = [k]
                        else:
                            key_groups[prefix].append(k)
                        keys_edit.remove(k)
        return keys_edit, key_groups

    @staticmethod
    def keyIsEnergy(key: str):
        return key.endswith("Eng")

    def modify(
        self, data: DataCollection, frame: int, data_cache: DataCollection, **kwargs
    ):
        if "log" not in data_cache.attributes:
            if not self.file_name:
                raise ValueError("Lammps log file name is empty")

            file_name = Path(self.file_name)
            file_names = glob.glob(str(file_name))
            if len(file_names) == 0:
                raise FileNotFoundError(f"{file_name} not found")

            log = lp.Log()
            for f in file_names:
                try:
                    log.parseLog(f)
                except Exception as e:
                    print(f"Error parsing {f}: {e}")
                    raise
            if "Step" not in log.keys():
                raise RuntimeError(
                    "Property 'Step' is required but not found in log file"
                )
            data_cache.attributes["log"] = log

        # Set attribute for current time step
        log = data_cache.attributes["log"]
        if "Timestep" in data.attributes:
            index = log["Step"] == data.attributes["Timestep"]
            try:
                index = np.where(index)[0][0]
                for key in log.keys():
                    data.attributes[f"lammps log {key}"] = log[key].iloc[index]
            except IndexError:
                pass

        # Set tables
        keys = list(log.keys())
        keys.remove("Step")
        keys.remove("Run")

        if self.group_components:
            keys, groups = self.groupComponents(keys)
            for g in groups:
                table = data.tables.create(
                    identifier=f"lammps log {g}",
                    plot_mode=DataTable.PlotMode.Line,
                    title=g,
                )

                table.x = table.create_property("Step", data=log["Step"])

                ydata = np.empty((len(log["Step"]), len(groups[g])))
                for i in range(len(groups[g])):
                    ydata[:, i] = log[groups[g][i]]
                if self.normalize_eng and self.keyIsEnergy(g):
                    ydata /= log["N"]
                table.y = table.create_property(key, data=ydata, components=groups[g])

        for key in keys:
            table = data.tables.create(
                identifier=f"lammps log {key}",
                plot_mode=DataTable.PlotMode.Line,
                title=key,
            )

            table.x = table.create_property("Step", data=log["Step"])

            ydata = np.expand_dims(log[key], axis=-1)
            if self.normalize_eng and self.keyIsEnergy(key):
                ydata /= log["N"]
            table.y = table.create_property(
                key,
                data=ydata,
                components=[key],
            )
