from esco.models import EducationLevel, EducationSchool, EducationCourse, Education
from neomodel import db

from skills import Domain
from skills.models.education import Course, Subject, Degree, School

with db.transaction:

    for degree in EducationLevel.objects.all():

        Degree(
            label=degree.name,
            uid=degree.id.hex
        ).save()


    for school in EducationSchool.objects.all():

        School(
            label=school.name,
            uid=school.id.hex
        ).save()


    for course in EducationCourse.objects.all():

        try:
            subject = Subject.nodes.get(label=course.name)
        except Subject.DoesNotExist:
            subject = Subject(
                label=course.name
            )
            subject.save()


    for edu in Education.objects.all():

        results, meta = db.cypher_query(
            'MATCH (subject:Subject)<-[:IS]-(c:Course)-[:IS]->(degree:Degree) WHERE degree.uid=$degree AND subject.label=$subject RETURN c',
            {'degree': edu.level.id.hex, 'subject': edu.course.name}
        )

        results = [Course.inflate(row[0]) for row in results]

        if len(results):
            course = results[0]
        else:
            course = Course()
            course.save()
            course.degree.connect(Degree.nodes.get(uid=edu.level.id.hex))
            course.subject.connect(Subject.nodes.get(label=edu.course.name))

            prio = 5
            for domain in edu.domains.all():
                course.domains.connect(Domain.nodes.get(label=domain.name), {'priority': prio})
                prio -= 1

        school = School.nodes.get(uid=edu.course.school.id.hex)
        course.schools.connect(school)
