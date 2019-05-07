#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Cyrille Favreau <cyrille.favreau@gmail.com>
#
# This file is part of pyPhaneron
# <https://github.com/favreau/pyPhaneron>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.


class CircuitExplorer(object):

    """ Color schemes """
    CIRCUIT_COLOR_SCHEME_NONE = 'None'
    CIRCUIT_COLOR_SCHEME_NEURON_BY_ID = 'By id'
    CIRCUIT_COLOR_SCHEME_NEURON_BY_LAYER = 'By layer'
    CIRCUIT_COLOR_SCHEME_NEURON_BY_MTYPE = 'By mtype'
    CIRCUIT_COLOR_SCHEME_NEURON_BY_ETYPE = 'By etype'
    CIRCUIT_COLOR_SCHEME_NEURON_BY_TARGET = 'By target'

    MORPHOLOGY_COLOR_SCHEME_NONE = 'None'
    MORPHOLOGY_COLOR_SCHEME_BY_SECTION_TYPE = 'By segment type'

    """ Morphology Types """
    MORPHOLOGY_SECTION_TYPE_ALL = 255
    MORPHOLOGY_SECTION_TYPE_SOMA = 1
    MORPHOLOGY_SECTION_TYPE_AXON = 2
    MORPHOLOGY_SECTION_TYPE_DENDRITE = 4
    MORPHOLOGY_SECTION_TYPE_APICAL_DENDRITE = 8

    """ Geometry quality """
    GEOMETRY_QUALITY_LOW = 0
    GEOMETRY_QUALITY_MEDIUM = 1
    GEOMETRY_QUALITY_HIGH = 2

    """ Defaults """
    DEFAULT_RESPONSE_TIMEOUT = 360

    """ Shading modes """
    SHADING_MODE_NONE = 0
    SHADING_MODE_DIFFUSE = 1
    SHADING_MODE_ELECTRON = 2
    SHADING_MODE_CARTOON = 3
    SHADING_MODE_ELECTRON_TRANSPARENCY = 4
    SHADING_MODE_PERLIN = 5
    SHADING_MODE_DIFFUSE_TRANSPARENCY = 6

    """ Simulation reports """
    REPORT_TYPE_NONE = 'Undefined'
    REPORT_TYPE_VOLTAGES_FROM_FILE = 'Voltages from file'
    REPORT_TYPE_VOLTAGES_FROM_DB = 'Voltages from DB'
    REPORT_TYPE_SPIKES = 'Spikes'

    """ User Data Types """
    USER_DATATYPE_NONE = 'Undefined'
    USER_DATATYPE_SIMULATION_OFFSET = 'Simulation offset'
    USER_DATATYPE_DISTANCE_TO_SOMA = 'Distance to soma'

    """ Circuit Explorer """
    def __init__(self, client):
        """
        Create a new Circuit Explorer instance
        """
        self._client = client.rockets_client
        self._brayns = client

    def __str__(self):
        """Return a pretTY-print of the class"""
        return "Circuit Explorer"

    def load_circuit(self, path, db_connection_string='', density=1.0, random_seed=0, targets=[], report='',
                     report_type=REPORT_TYPE_NONE, user_data_type=USER_DATATYPE_NONE, synchronous_mode=True,
                     circuit_color_scheme=CIRCUIT_COLOR_SCHEME_NONE, mesh_folder='', mesh_filename_pattern='',
                     mesh_transformation=False, radius_multiplier=1, radius_correction=0, load_soma=True,
                     load_axon=True, load_dendrite=True, load_apical_dendrite=True, use_sdf=False,
                     dampen_branch_thickness_changerate=True, use_metaballs_for_soma=False, metaballs_section_samples=5,
                     metaballs_grid_size=20, metaballs_threshold=1,
                     morphology_color_scheme=MORPHOLOGY_COLOR_SCHEME_NONE, morphology_quality=GEOMETRY_QUALITY_HIGH,
                     max_distance_to_soma=1e6, cell_clipping=False):

        props = dict()
        props['000DbConnectionString'] = db_connection_string
        props['001Density'] = density
        props['002RandomSeed'] = random_seed

        targets_as_string=''
        for target in targets:
            if targets_as_string != '':
                targets_as_string += ','
            targets_as_string += target
        props['010Targets'] = targets_as_string

        props['020Report'] = report
        props['021ReportType'] = report_type
        props['022UserDataType'] = user_data_type
        props['023SynchronousMode'] = synchronous_mode

        props['030CircuitColorScheme'] = circuit_color_scheme

        props['040MeshFolder'] = mesh_folder
        props['041MeshFilenamePattern'] = mesh_filename_pattern
        props['042MeshTransformation'] = mesh_transformation

        props['050RadiusMultiplier'] = radius_multiplier
        props['051RadiusCorrection'] = radius_correction
        props['052SectionTypeSoma'] = load_soma
        props['053SectionTypeAxon'] = load_axon
        props['054SectionTypeDendrite'] = load_dendrite
        props['055SectionTypeApicalDendrite'] = load_apical_dendrite

        props['060UseSdfgeometry'] = use_sdf
        props['061DampenBranchThicknessChangerate'] = dampen_branch_thickness_changerate

        props['070RealisticSoma'] = use_metaballs_for_soma
        props['071MetaballsSamplesFromSoma'] = metaballs_section_samples
        props['072MetaballsGridSize'] = metaballs_grid_size
        props['073MetaballsThreshold'] = metaballs_threshold

        props['080MorphologyColorScheme'] = morphology_color_scheme

        props['090MorphologyQuality'] = morphology_quality
        props['091MaxDistanceToSoma'] = max_distance_to_soma
        props['100CellClipping'] = cell_clipping

        return self._brayns.add_model(path=path, loader_properties=props)

    def set_material(self, model_id, material_id, diffuse_color=[1.0, 1.0, 1.0],
                     specular_color=[1.0, 1.0, 1.0], specular_exponent=20.0, opacity=1.0,
                     reflection_index=0.0, refraction_index=1.0, simulation_data_cast=True,
                     glossiness=1.0, intensity=1.0, shading_mode=SHADING_MODE_NONE, emission=0.0, clipped=False):
        params = dict()
        params['modelId'] = model_id
        params['materialId'] = material_id
        params['diffuseColor'] = [diffuse_color[0] * intensity, diffuse_color[1] * intensity,
                                  diffuse_color[2] * intensity]
        params['specularColor'] = specular_color
        params['specularExponent'] = specular_exponent
        params['reflectionIndex'] = reflection_index
        params['opacity'] = opacity
        params['refractionIndex'] = refraction_index
        params['emission'] = emission
        params['glossiness'] = glossiness
        params['simulationDataCast'] = simulation_data_cast
        params['shadingMode'] = shading_mode
        params['clipped'] = clipped

        return self._client.request("setMaterial", params=params,
                                    response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def set_materials(self, model_ids, material_ids, diffuse_colors, specular_colors, specular_exponents, opacities,
                      reflection_indices, refraction_indices, simulation_data_casts, glossinesses, shading_modes,
                      emissions, clips):
        params = dict()
        params['modelIds'] = model_ids
        params['materialIds'] = material_ids

        dc = list()
        for diffuse in diffuse_colors:
            for k in range(3):
                dc.append(diffuse[k])
        params['diffuseColors'] = dc

        sc = list()
        for specular in specular_colors:
            for k in range(3):
                sc.append(specular[k])
        params['specularColors'] = sc

        params['specularExponents'] = specular_exponents
        params['reflectionIndices'] = reflection_indices
        params['opacities'] = opacities
        params['refractionIndices'] = refraction_indices
        params['emissions'] = emissions
        params['glossinesses'] = glossinesses
        params['simulationDataCasts'] = simulation_data_casts
        params['shadingModes'] = shading_modes
        params['clips'] = clips

        return self._client.request("setMaterials", params=params,
                                    response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def set_transfer_function(self,
                              palette, data_range=(0, 255), contribution=1.0, intensity=1.0, emission=(0.0, 0.0, 0.0)):
        ml = self._client.transfer_function
        ml.diffuse = []
        ml.contribution = []
        ml.emission = []
        for color in palette:
            alpha = 1.0
            if len(color) == 4:
                alpha = color[3]
            ml.diffuse.append((color[0]*intensity, color[1]*intensity, color[2]*intensity, alpha))
            ml.contribution.append(contribution)
            ml.emission.append(emission)
        ml.range = data_range
        ml.commit()

    def load_from_cache(self, name, path):
        """
        Loads a model from a cache file
        :param name: Name of the loaded model
        :param path: Path of the cache file
        :return: Result of the request submission
        """
        params = dict()
        params['name'] = name
        params['path'] = path
        return self._client.request('loadModelFromCache', params=params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def save_to_cache(self, model_id, path):
        """
        Saves a model to the specified cache file
        :param model_id: Id of the model to save
        :param path: Path of the cache file
        :return: Result of the request submission
        """
        params = dict()
        params['modelId'] = model_id
        params['path'] = path
        return self._client.request('saveModelToCache', params=params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def set_connections_per_value(self, model_id, frame, value, epsilon):
        """
        Saves a model to the specified cache file
        :param model_id: Id of the model to save
        :param frame: Simulation frame number
        :param value: Value for which connections should be created
        :param epsilon: Tolerance for the value
        :return: Result of the request submission
        """
        params = dict()
        params['modelId'] = model_id
        params['frame'] = frame
        params['value'] = value
        params['epsilon'] = epsilon
        return self._client.request('setConnectionsPerValue', params=params,
                                    response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def set_metaballs_per_simulation_value(self, model_id, frame, value, epsilon, grid_size, threshold):
        """
        Saves a model to the specified cache file
        :param model_id: Id of the model to save
        :param frame: Simulation frame number
        :param value: Value for which connections should be created
        :param epsilon: Tolerance for the value
        :param grid_size: Size of the metaballs grid
        :param threshold: Points in 3D space that fall below the threshold (when run through the
               function) are ONE, while points above the threshold are ZERO
        :return: Result of the request submission
        """
        params = dict()
        params['modelId'] = model_id
        params['frame'] = frame
        params['value'] = value
        params['epsilon'] = epsilon
        params['gridSize'] = grid_size
        params['threshold'] = threshold
        return self._client.request('setMetaballsPerSimulationValue', params=params,
                                    response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def get_focal_distance(self, coordinates=(0.5, 0.5)):
        """
        Return the focal distance for the specified normalized coordinates in the image
        :param coordinates: Coordinates in the image
        :return: Focal distance
        """
        target = self._client.inspect(position=coordinates)['position']
        origin = self._client.camera.origin.data
        v = [0, 0, 0]
        for k in range(3):
            v[k] = float(target[k]) - float(origin[k])
        import math
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])

    def set_material_extra_attributes(self, model_id):
        """
        Adds extra attributes to all materials in the model
        :param model_id: Id of the model
        """
        params = dict()
        params['modelId'] = model_id
        return self._client.request('setMaterialExtraAttributes', params=params,
                                    response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def set_default_transfer_function(self, alpha=1, intensity=1, display_palette=False):
        """
        Applies the default transfer function
        :param alpha: Alpha applied to every color in the map
        :param intensity: Alpha applied to every color in the map
        :param display_palette: Shows the palette in the notebook if %matplotlib inline is specified
        """
        points = dict()
        colormap_size = 256
        range_min = -80.0
        range_max = -10.0
        colormap_range = range_max - range_min
        delta = colormap_size / colormap_range

        points[int((-80.0 - range_min) * delta)] = [1.0, 0.0, 0.0, 0.0]
        points[int((-77.181205 - range_min) * delta)] = [0.023529, 0.023529, 0.6549020, 0.05]
        points[int((-72.06669 - range_min) * delta)] = [0.141176, 0.529412, 0.9607843, 0.16]
        points[int((-70.2 - range_min) * delta)] = [0.388235, 0.345098, 0.7137255, 0.22]
        points[int((-67.4 - range_min) * delta)] = [0.2, 0.0, 0.09, 0.3]
        points[int((-50.67785 - range_min) * delta)] = [0.858824, 0.674510, 0.0000000, 0.4]
        points[int((-31.47 - range_min) * delta)] = [0.964706, 1.000000, 0.6313725, 0.8]
        points[int((-10 - range_min) * delta)] = [1.0, 1.0, 1.0, 1.0]

        sorted_points = sorted(points.items())

        X = []
        for p in sorted_points:
            X.append(p[0])

        reds = []
        greens = []
        blues = []
        alphas = []
        for p in sorted_points:
            reds.append(p[1][0])
            greens.append(p[1][1])
            blues.append(p[1][2])
            alphas.append(p[1][3])

        import numpy as np
        from scipy.interpolate import interp1d

        k = 'linear'
        x = np.array(X)
        f_red = interp1d(x, np.array(reds), kind=k)
        f_green = interp1d(x, np.array(greens), kind=k)
        f_blue = interp1d(x, np.array(blues), kind=k)
        f_alpha = interp1d(x, np.array(alphas), kind=k)

        contributions = []
        diffuses = []
        emissions = []
        palette = []

        for i in range(colormap_size):
            light_intensity = 0
            c = [intensity * float(f_red(i)), float(intensity * f_green(i)),
                 float(intensity * f_blue(i)), alpha]
            palette.append(c)
            diffuses.append(c)
            emissions.append([light_intensity, light_intensity, light_intensity])
            contributions.append(1)

        self._client.transfer_function.diffuse = diffuses
        self._client.transfer_function.emission = emissions
        self._client.transfer_function.contribution = contributions
        self._client.transfer_function.range = [range_min, range_max]
        self._client.transfer_function.commit()

        if display_palette:
            import matplotlib.pyplot as plt
            import seaborn as sns
            plt.plot(x, f_red(x), '+-', x, f_green(x), '+-', x, f_blue(x), '+-', x, f_alpha(x),
                     '+-')
            plt.show()
            sns.palplot(palette)

    def load_cells(self, connection_string, sql_cells, sql_morphologies, name, use_sdf=False):
        params = dict()
        params['connectionString'] = connection_string
        params['name'] = name
        params['sqlCell'] = sql_cells
        params['sqlMorphology'] = sql_morphologies
        params['sdf'] = use_sdf
        result = self._client.request('loadCells', params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)
        if not result['success']:
            raise Exception(result['error'])

    def load_cells_as_instances(self, connection_string, sql_statement, name, description, morphology_folder,
                                morphology_extension):
        params = dict()
        params['connectionString'] = connection_string
        params['sqlStatement'] = sql_statement
        params['name'] = name
        params['description'] = description
        params['description'] = description
        params['morphologyFolder'] = morphology_folder
        params['morphologyExtension'] = morphology_extension
        result = self._client.request('loadCellsAsInstances', params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)
        if not result['success']:
            raise Exception(result['error'])

    def load_somas(self, connection_string, name='', sql_statement='', radius=1.0,
                           show_orientations=False):
        params = dict()
        params['connectionString'] = connection_string
        params['name'] = name
        params['sqlStatement'] = sql_statement
        params['radius'] = radius
        params['showOrientations'] = show_orientations
        result = self._client.request('loadSomas', params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)
        if not result['success']:
            raise Exception(result['error'])

    def attach_circuit_simulation_handler(self, model_id, circuit_configuration, report_name, synchronous_mode=True):
        params = dict()
        params['modelId'] = model_id
        params['circuitConfiguration'] = circuit_configuration
        params['reportName'] = report_name
        params['synchronousMode'] = synchronous_mode
        return brayns.request('attachCircuitSimulationHandler', params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def set_camera(self, origin, direction, up):
        params = dict()
        params['origin'] = origin
        params['direction'] = direction
        params['up'] = up
        return self._client.request('setCamera', params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def get_camera(self):
        return self._client.request('getCamera', response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def focal_distance_at(self, position):
        inspect = self._client.inspect(position)
        if inspect['hit']:
            p = inspect['position']
            o = self._client.camera['position'].data
            import math
            return math.sqrt(math.pow(p[0] - o[0], 2) + math.pow(p[1] - o[1], 2) + math.pow(p[2] - o[2], 2))
        else:
            return 1e6

    def add_grid(self, min_value, max_value, interval, radius=1.0, opacity=0.5, show_axis=True, colored=True):
        params = dict()
        params['minValue'] = min_value
        params['maxValue'] = max_value
        params['steps'] = interval
        params['radius'] = radius
        params['planeOpacity'] = opacity
        params['showAxis'] = show_axis
        params['useColors'] = colored
        return self._client.request('addGrid', params, response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)

    def export_frames_to_disk(self, path, animation_frames, camera_definitions, image_format='png',
                              quality=100, samples_per_pixel=1, start_frame=0):
        params = dict()
        params['path'] = path
        params['format'] = image_format
        params['quality'] = quality
        params['spp'] = samples_per_pixel
        params['startFrame'] = start_frame
        params['animationInformation'] = animation_frames
        values = list()
        for camera_definition in camera_definitions:
            for i in range(3):
                values.append(camera_definition[0][i])
            for i in range(3):
                values.append(camera_definition[1][i])
            for i in range(3):
                values.append(camera_definition[2][i])
        params['cameraInformation'] = values
        return self._client.request('exportFramesToDisk', params,
                                    response_timeout=self.DEFAULT_RESPONSE_TIMEOUT)
