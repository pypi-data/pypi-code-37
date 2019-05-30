import nanome
from nanome.util import Logs, Octree, Color

SURROUNDING_DISTANCE = 5  # Angstroms

class LigandFocus(nanome.PluginInstance):
    def on_run(self):
        self.request_workspace(self.on_workspace_received)

    def on_workspace_received(self, workspace):
        # Find ligand (smallest molecule, with only hetatoms and name != HOH here)
        smallest_residue = None
        smallest_atom_count = 0
        for complex in workspace.complexes:
            for residue in complex.residues:
                if residue.molecular.name == "HOH":
                    continue

                atom_count = 0
                het_only = True
                for atom in residue.atoms:
                    atom_count += 1
                    if not atom.molecular.is_het:
                        het_only = False
                        break

                if not het_only:
                    continue

                if smallest_atom_count == 0 or atom_count < smallest_atom_count:
                    smallest_residue = residue
                    smallest_residue.complex = complex  # Save complex for its transformation matrix
                    smallest_atom_count = atom_count

        if smallest_residue == None:
            return

        self.select_site(smallest_residue, workspace)

    def select_site(self, ligand, workspace):
        ligand_atoms = Octree()
        structures_to_update = []
        to_ignore = []

        # Add all ligand atoms to an Octree
        complex_local_to_workspace_matrix = ligand.complex.transform.get_complex_to_workspace_matrix()
        for atom in ligand.atoms:
            atom_absolute_pos = complex_local_to_workspace_matrix * atom.molecular.position
            ligand_atoms.add(atom, atom_absolute_pos)
            atom.rendering.selected = True
            atom.rendering.surface_rendering = False
            atom.rendering.atom_mode = nanome.structure.Atom.AtomRenderingMode.BallStick
            to_ignore.append(atom)

        # Find all atoms near the ligand, using the Octree
        found_atoms = []
        for complex in workspace.complexes:
            complex_local_to_workspace_matrix = complex.transform.get_complex_to_workspace_matrix()
            structures_to_update.append(complex)
            for atom in complex.atoms:
                if atom in to_ignore:
                    continue

                atom_absolute_pos = complex_local_to_workspace_matrix * atom.molecular.position
                found_atoms.clear()
                ligand_atoms.get_near_append(atom_absolute_pos, SURROUNDING_DISTANCE, found_atoms, 1)

                if len(found_atoms) > 0:
                    atom.rendering.selected = True
                    atom.rendering.surface_rendering = True
                    atom.rendering.atom_mode = nanome.structure.Atom.AtomRenderingMode.Stick
                    atom.rendering.atom_color = Color.White()
                else:
                    atom.rendering.selected = False
                    atom.rendering.surface_rendering = False
                    atom.rendering.set_visible(False)

                complex.rendering.set_surface_needs_redraw()
        
        def on_update_done():
            pass
            # self.zoom_on_structures(ligand)

        self.update_structures_deep(structures_to_update, on_update_done)

def main():
    plugin = nanome.Plugin("Ligand Focus", "On-click focus on a ligand and its binding site", "Utilities", False)
    plugin.set_plugin_class(LigandFocus)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()