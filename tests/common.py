'''
Common functions for tests.

This module uses additional file called config.py (located in the tests/
directory) which defines th BLENDER_EXEC_PATH - a string with a path to the
blender executable.

If BLENDER_EXEC_PATH is not specified the test script tries to run blender with
`blender` command.

The config.py file is blacklisted in .gitignore because it can be different on
different devices.
'''
import typing as tp
import subprocess
try:
    from .config import BLENDER_EXEC_PATH
except:
    BLENDER_EXEC_PATH = 'blender'


def blender_run_script(script, *args):
    command = [BLENDER_EXEC_PATH, '-b', '--python', script, '--', *args]
    subprocess.call(command)

def assert_is_vector(vect: tp. Any, length: int, types: tp.Tuple):
    assert type(vect) is list
    assert len(vect) == length
    assert all([isinstance(i, types) for i in vect])


def assert_is_model(a: tp.Dict):
    '''Check if the input is a valid model'''
    assert type(a) is dict
    assert set(a.keys()) == {'format_version', 'minecraft:geometry'}

    assert a['format_version'] == "1.12.0"

    geometries = a['minecraft:geometry']
    assert type(geometries) is list
    assert len(geometries) > 0
    
    # minecraft:geometry
    for geometry in geometries:
        assert type(geometry) is dict
        assert set(geometry.keys()) == {'description', 'bones'}
        desc = geometry['description']
        bones = geometry['bones']

        # minecraft:geometry -> description
        assert type(desc) is dict
        assert set(desc.keys()) == {
            'identifier', 'texture_width',
            'texture_height', 'visible_bounds_width', 'visible_bounds_height',
            'visible_bounds_offset'
        }
        assert type(desc['identifier']) is str
        assert type(desc['texture_width']) is int
        assert type(desc['texture_height']) is int
        assert isinstance(desc['visible_bounds_width'], (float, int))
        assert isinstance(desc['visible_bounds_height'], (float, int))
        assert_is_vector(desc['visible_bounds_offset'], 3, (int, float))

        # minecraft:geometry -> bones
        assert type(bones) is list
        for bone in bones:
            assert type(bone) is dict

            assert set(bone.keys()) <= {  # acceptable keys
                'name', 'cubes', 'pivot', 'rotation', 'parent', 'locators'
            }
            assert set(bone.keys()) >= {  # obligatory keys
                'name', 'cubes', 'pivot', 'rotation'
            }
            assert type(bone['name']) is str

            assert_is_vector(bone['pivot'], 3, (int, float))
            assert_is_vector(bone['rotation'], 3, (int, float))
            if 'parent' in bone:
                assert type(bone['parent']) is str
            # minecraft:geometry -> bones -> locators
            if 'locators' in bone:
                assert type(bone['locators']) is dict
                for locator_name, locator in bone['locators'].items():
                    assert type(locator_name) is str
                    assert_is_vector(locator, 3, (int, float))
            # minecraft:geometry -> bones -> cubes
            assert type(bone['cubes']) is list
            for cube in bone['cubes']:
                assert type(cube) is dict
                assert set(cube.keys()) <= {  # acceptable keys
                    'uv', 'size', 'origin', 'pivot', 'rotation',
                    'mirror'
                }
                assert set(cube.keys()) >= {  # obligatory keys
                    'uv', 'size', 'origin', 'pivot', 'rotation'
                }
                assert_is_vector(cube['uv'], 2, (int, float))
                assert_is_vector(cube['size'], 3, (int, float))
                assert_is_vector(cube['origin'], 3, (int, float))
                assert_is_vector(cube['pivot'], 3, (int, float))
                assert_is_vector(cube['rotation'], 3, (int, float))
                if 'mirror' in cube:
                    assert type(cube['mirror']) is bool
