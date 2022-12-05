
import blender_plot as bp
import bpy


class TestScene:
    def test_create_scene(self):
        import gc
        gc.collect()

        # we do not touch the default blender scene
        assert len(bpy.data.scenes) == 1

        scene1 = bp.DefaultScene()
        assert len(bpy.data.scenes) == 2
        assert scene1.active

        scene2 = bp.DefaultScene()
        assert len(bpy.data.scenes) == 3
        assert scene2.active

    def test_delete_scene(self):
        import gc
        gc.collect()

        assert len(bpy.data.scenes) == 1

        scene1 = bp.DefaultScene()
        scene2 = bp.DefaultScene()

        assert len(bpy.data.scenes) == 3

        # delete the scene
        del scene2
        gc.collect()

        assert len(bpy.data.scenes) == 2

    def test_clear_scene(self):
        scene1 = bp.DefaultScene()

        # TODO: do something with scene1

        scene2 = bp.DefaultScene()
        scene1.clear()
        assert scene1.active

        # TODO: test if scene1 is back to default

    def test_save_scene(self, tmp_path):
        filepath = tmp_path / "scene.blend"

        assert not filepath.is_file()

        scene = bp.DefaultScene()
        scene.save(filepath)

        assert filepath.is_file()

    def test_load_scene(self, tmp_path):
        filepath = tmp_path / "scene.blend"

        assert not filepath.is_file()

        scene = bp.DefaultScene()

        # TODO: do something with the scene

        scene.save(filepath)

        assert filepath.is_file()

        scene.clear()
        scene.load(filepath)

        # TODO: check if things we did are same

        assert filepath.is_file()

    def test_render_scene(self, tmp_path):
        filepath = tmp_path / "scene.png"

        scene = bp.DefaultScene()
        scene.render(filepath)

        assert filepath.is_file()
