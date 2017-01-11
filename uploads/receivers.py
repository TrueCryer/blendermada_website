def remove_uploaded_files(sender, instance, **kwargs):
    instance.uploaded_file.delete()
    instance.storage.delete()
    instance.image.delete()


def remove_scene_files(sender, instance, **kwargs):
    instance.file.delete()
    instance.image.delete()
    instance.thumb_big.delete()
    instance.thumb_small.delete()
