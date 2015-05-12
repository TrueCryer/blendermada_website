from brabeion.sites import badges
from brabeion.base import Badge, BadgeAwarded, BadgeDetail


class MaterialMakerBadge(Badge):
    slug = "material_maker"
    levels = [
        BadgeDetail("Wooden", "Upload at least 1 material"),
        BadgeDetail("Bronze", "Upload at least 5 materials"),
        BadgeDetail("Silver", "Upload at least 20 materials"),
        BadgeDetail("Gold", "Upload at least 50 materials"),
        BadgeDetail("Platinum", "Upload at least 100 materials"),
    ]
    events = [
        "material_maker_awarded",
    ]
    multiple = False
    def award(self, **state):
        user = state["user"]
        materials = user.materials.count()
        print(materials)
        if materials >= 100:
            return BadgeAwarded(level=5)
        elif materials >= 50:
            return BadgeAwarded(level=4)
        elif materials >= 20:
            return BadgeAwarded(level=3)
        elif materials >= 5:
            return BadgeAwarded(level=2)
        elif materials >= 1:
            return BadgeAwarded(level=1)


badges.register(MaterialMakerBadge)
