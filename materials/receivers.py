def update_downloads(sender, **kwargs):
    kwargs.get('instance').material.update_downloads()


def update_rating(sender, **kwargs):
    kwargs.get('instance').material.update_rating()
