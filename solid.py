from __future__ import division

import argparse
import numpy as np
import precice

parser = argparse.ArgumentParser()
parser.add_argument("configurationFileName",
                    help="Name of the xml config file.", type=str)
parser.add_argument("participantName", help="Name of the solver.", type=str)

try:
    args = parser.parse_args()
except SystemExit:
    print("")
    print("Usage: python ./solverdummy precice-config participant-name")
    quit()

configuration_file_name = args.configurationFileName
participant_name = args.participantName

if participant_name == 'Fluid':
    write_data_name = 'Force'
    read_data_name = 'Data-Two'
    mesh_name = 'Fluid-Mesh'

if participant_name == 'Solid':
    read_data_name = 'Force'
    write_data_name = 'Data-Two'
    mesh_name = 'SolverTwo-Mesh'

num_vertices = 1  # Number of vertices

solver_process_index = 0
solver_process_size = 1
configuration_file_name="precice-config.xml"
participant_name="solid"
participant = precice.Participant(participant_name, configuration_file_name,
                                  solver_process_index, solver_process_size)

#assert (participant.requires_mesh_connectivity_for(mesh_name) is False)

vertices = np.zeros((num_vertices, participant.get_mesh_dimensions(mesh_name)))
read_data = np.zeros((num_vertices, participant.get_data_dimensions(mesh_name, read_data_name)))
write_data = np.zeros((num_vertices, participant.get_data_dimensions(mesh_name, write_data_name)))

for x in range(num_vertices):
    for y in range(participant.get_mesh_dimensions(mesh_name)):
        vertices[x, y] = x

    for y in range(participant.get_data_dimensions(mesh_name, read_data_name)):
        read_data[x, y] = x

    for y in range(participant.get_data_dimensions(mesh_name, write_data_name)):
        write_data[x, y] = x

vertex_ids = participant.set_mesh_vertices(solid, vertices)


precice_dt=participant.initialize()
my_dt=precice_dt

while participant.is_coupling_ongoing():
    if participant.requires_writing_checkpoint():
        print("DUMMY: Writing iteration checkpoint")

    dt = participant.get_max_time_step_size(precice_dt,my_dt)
    read_data = participant.read_data(fluid,force, vertex_ids, dt)
    print(read_data)
    write_data = 1

    participant.write_data(fluif, displacement, vertex_ids, write_data)

    print("DUMMY: Advancing in time")
    participant.advance(dt)

    if participant.requires_reading_checkpoint():
        print("DUMMY: Reading iteration checkpoint")

participant.finalize()
print("DUMMY: Closing python solver dummy...")
