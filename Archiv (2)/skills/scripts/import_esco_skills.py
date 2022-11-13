from esco.models import Skill as ESCOSkill, SkillToFunction, SkillToPersonalityType, PERSONALITY_TYPE_CHOICES
from esco.sparql import ESCOSparql

from skills import Domain, Function, PersonalityType
from x28_ontology.models import Occupation
from skills import OntologyOccupation
from skills import ESCOSkill as ESCONodeSkill
from core.models import Domain as OldDomain

# this script imports 'old' skill data into the new graph-db
# requires the skill-database to be empty, but ESCOSkill nodes to be populated
# occupations are mapped
from neomodel import db

from skills import Skill, SKILL_TYPE_ACTIVITY, SKILL_TYPE_KNOWLEDGE, SKILL_TYPE_SOCIAL


def type_for_esco_skill(skill):
    if skill.type == 1:
        return SKILL_TYPE_ACTIVITY
    elif skill.type == 2:
        return SKILL_TYPE_KNOWLEDGE
    else:
        return SKILL_TYPE_SOCIAL


def get_or_create_ontology_occupation(esco_ontology_occ):

    try:
        return OntologyOccupation.nodes.get(ontology_id=esco_ontology_occ.id)
    except OntologyOccupation.DoesNotExist:
        occ = OntologyOccupation(
            ontology_id=esco_ontology_occ.id,
            label=Occupation.objects.get(id=esco_ontology_occ.id).name
        )
        occ.save()
        return occ


sparql = ESCOSparql()

with db.transaction:

    functions = {}

    # import functions and domains
    for domain in OldDomain.objects.filter(is_other=False):
        node = Domain(label=domain.name)
        node.save()
        for function in domain.functions.filter(is_other=False):
            fun_node = Function(label=function.name)
            fun_node.save()
            node.functions.connect(fun_node)
            functions[function.id] = fun_node


    qs = ESCOSkill.objects.filter(display=True)
    total = qs.count()
    count = 0


    for esco_skill in qs:

        count += 1
        print(f'importing skill {count}/{total}')

        skill = Skill(
            uid=esco_skill.id.hex,
            label=esco_skill.label,
            type=type_for_esco_skill(esco_skill),
            esco_concept_url=esco_skill.url
        )

        skill.save()

        parents = sparql.get_parents(esco_skill.url)
        for parent in parents:
            if int(parent[1].value) == 1: # only direct parents
                if parent := ESCONodeSkill.nodes.get_or_none(concept_url=parent[0].value):
                    skill.broader.connect(parent)
                else:
                    print(f'could not find parent skill')

        for occ in esco_skill.occupations.all(): # find all esco-occupations for skill
            for ontology_occ in occ.ontology_occupations.all(): # find all linked x28 occupations
                try:
                    skill.occupations.connect(
                        get_or_create_ontology_occupation(ontology_occ) # find/create node for x28 occupation
                    )
                except BaseException as e:
                    # ignore errors due to inconsistent data for now
                    # TODO: change for production
                    print(e)
                    pass

        # connect functions
        for rel in SkillToFunction.objects.filter(skill=esco_skill):
            fun_node = functions[rel.function.id]
            skill.functions.connect(fun_node, {'priority': rel.match})

        for rel in SkillToPersonalityType.objects.filter(skill=esco_skill):
            code = dict(PERSONALITY_TYPE_CHOICES)[rel.personality_type]
            skill.personality_types.connect(
                PersonalityType.nodes.get(code=code),
                {'priority': rel.match}
            )
