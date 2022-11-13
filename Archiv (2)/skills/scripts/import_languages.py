from neomodel import db
from core.models import Language
from skills import Skill

with db.transaction:
    for lang in Language.objects.all():
        if not Skill.nodes.get_or_none(type='language', label=lang.name):
            Skill(
                type='language',
                label=lang.name
            ).save()
