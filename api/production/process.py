from django.utils import timezone

from . import models


class SaveDataToFile:

    @staticmethod
    def save_teacher_training(report_annual, type_report, user, row):
        models.TeacherTraining.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            user=user,
            name=row[1],
            institute=row[2],
            type_activity=row[3],
            hours=row[4],
        )

    @staticmethod
    def save_exchange_activity(report_annual, type_report, user, row):
        models.ExchangeActivity.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            user=user,
            division=row[1],
            activity=row[2],
            ies=row[3],
            country=row[4],
        )

    @staticmethod
    def save_academic_events(report_annual, type_report, user, row):
        models.AcademicEvents.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            user=user,
            name=row[1],
            institute=row[2],
            country=row[3],
            range_date=row[4],
            type_activity=row[5],
        )

    @staticmethod
    def save_academic_collaboration(report_annual, type_report, user, row):
        models.AcademicCollaboration.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            user=user,
            name=row[1],
            institutions=row[2],
            activities=row[3],
        )

    @staticmethod
    def save_project_collaboration(report_annual, type_report, user, row):
        models.ProjectCollaboration.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            user=user,
            name=row[1],
            organizations=row[2],
            sector=row[3],
        )

    @staticmethod
    def save_magazine_publications(report_annual, type_report, users, row):
        instance = models.MagazinePublications.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            title=row[2],
            magazine_name=row[3],
            number=row[4],
            volume=row[5],
            pages=row[6],
            is_indexed_magazine=row[7],
            type_job=row[8],
        )

        for user in users:
            instance.user.add(user)

        instance.save()

    @staticmethod
    def save_electronic_journals(report_annual, type_report, users, row):
        instance = models.ElectronicJournals.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            title=row[2],
            magazine_name=row[3],
            number=row[4],
            volume=row[5],
            pages=row[6],
            doi=row[7],
            type_job=row[8],
        )

        for user in users:
            instance.user.add(user)

        instance.save()

    @staticmethod
    def save_newspaper_publication(report_annual, type_report, users, row):
        list_date = row[1].split('/')
        date_string = list_date[0] + "-" + list_date[2] + "-" + list_date[1]
        date = timezone.datetime.strptime(date_string, '%Y-%m-%d')

        instance = models.NewspaperPublication.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            date=date,
            title=row[2],
            newspaper_name=row[3],
            section=row[4],
            pages=row[5],
            type_job=row[6],
        )

        for user in users:
            instance.user.add(user)

        instance.save()

    @staticmethod
    def save_published_books(report_annual, type_report, users, row):
        instance = models.PublishedBooks.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            title=row[2],
            edition=row[3],
            place=row[4],
            editorial=row[5],
            isbn=row[6],
            type_job=row[7],
        )

        for user in users:
            instance.user.add(user)

        instance.save()

    @staticmethod
    def save_chapters_books(report_annual, type_report, users, departament, row):
        instance = models.ChaptersBooks.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            departament=departament,
            name=row[2],
            bibliographic_file=row[3],
        )

        for user in users:
            instance.user.add(user)

        instance.save()

    @staticmethod
    def save_book_reviews(report_annual, type_report, user, row):
        models.BookReviews.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            user=user,
            title=row[2],
            book=row[3],
            publication=row[4],
            number=row[5],
            volume=row[6],
            pages=row[7],
        )

    @staticmethod
    def save_published_lectures(report_annual, type_report, users, row):
        instance = models.PublishedLectures.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            title=row[2],
            editor=row[3],
            ed=row[4],
            congress=row[5],
            pages=row[6],
            place=row[7],
            editorial=row[8],
            type_job=row[9],
        )

        for user in users:
            instance.user.add(user)

        instance.save()

    @staticmethod
    def save_unpublished_lectures(report_annual, type_report, users, row):
        instance = models.UnpublishedLectures.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            title=row[2],
            present=row[3],
            congress=row[4],
            city=row[5],
            country=row[6],
            institute=row[7],
            type_job=row[8],
        )

        for user in users:
            instance.user.add(user)

        instance.save()

    @staticmethod
    def save_research_projects(report_annual, type_report, user, departament, row):
        models.ResearchProjects.objects.create(
            annual_report=report_annual,
            type_report=type_report,
            user=user,
            departament=departament,
            name=row[1],
            participants=row[3],
            approval=row[4],
            validity=row[5],
            section=row[6],
            means=row[7],
            line=row[8],
        )
