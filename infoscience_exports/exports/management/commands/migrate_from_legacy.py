from django.core.management.base import BaseCommand

from exporter.models import SettingsModel
from exports.models import Export, User

"""
dump with 
manage.py dumpdata -o ./exports_from_32.json exporter

load with
make load-dump
"""


class Command(BaseCommand):

    help = "Migrate exports from infoscience-legacy base to the new format"

    # A command must define handle()
    def handle(self, *args, **options):
        import pdb

        for exporter in SettingsModel.objects.all():
            s = exporter.settings_as_dict()

            self.stdout.write("doing {}...".format(exporter.id))
            new_export = Export()

            new_export.name = "from old export {}".format(exporter.id)

            # TODO created_at, updated_at
            new_export.created_at = exporter.created_at
            new_export.updated_at = exporter.updated_at

            # url
            new_export.url = exporter.build_url()

            # format type
            if 'format_type' in s and s['format_type']:
                if 'ENACFULL' in s['format_type']:
                    new_export.show_thumbnail = True
                    new_export.formats_type = 'DETAILED'
                    new_export.show_summary = True
                    new_export.show_article_volume = True
                    new_export.show_article_volume_number = True
                    new_export.show_article_volume_pages = True
                    new_export.show_thesis_directors = True
                    new_export.show_thesis_pages = True
                    new_export.show_report_working_papers_pages = True
                    new_export.show_conf_proceed_place = True
                    new_export.show_conf_proceed_date = True
                    new_export.show_conf_paper_journal_name = True
                    new_export.show_book_isbn = True
                    new_export.show_book_doi = True
                    new_export.show_book_chapter_isbn = True
                    new_export.show_book_chapter_doi = True
                    new_export.show_patent_status = True
                else:
                    if 'short' in s['format_type']:
                        new_export.formats_type = 'SHORT'
                    elif 'detailed' in s['format_type']:
                        new_export.formats_type = 'DETAILED'
                    elif 'full' in s['format_type']:
                        new_export.formats_type = 'DETAILED'
                        new_export.show_summary = True
                    if '_authors' in s['format_type']:
                        new_export.show_linkable_authors = True



            # group by
            # TODO:
            if 'group_by_year_seperate_pending' in s and s['group_by_year_seperate_pending']:
                new_export.show_pending_publications = True

            new_export.groupsby_type = 'NONE'
            new_export.groupsby_doc = 'NONE'
            new_export.groupsby_year = 'NONE'

            if 'group_by_first' in s:
                if s['group_by_first'] == 'year':
                    if 'group_by_year_display_headings' in s and s['group_by_year_display_headings']:
                        new_export.groupsby_type = 'YEAR_TITLE'
                    if 'group_by_second' in s and s['group_by_second'] == 'doctype':
                        new_export.groupsby_doc = 'DOC_TITLE'
                elif s['group_by_first'] == 'doctype':
                    new_export.groupsby_type = 'DOC_TITLE'
                    if 'group_by_second' in s and s['group_by_second'] == 'year':
                        new_export.groupsby_year = 'YEAR_TITLE'

            # bullets
            if 'format_bullet_order' in s and s['format_bullet_order']:
                new_export.show_detailed = True

            if 'format_bullets' in s and s['format_bullets']:
                if 'format_bullets_type' in s:
                    if s['format_bullets_type'] == 'text':
                        if 'format_bullet_text' in s and s['format_bullet_text']:
                            if s['format_bullet_text'] == '*':
                                new_export.bullets_type = 'CHARACTER_STAR'
                            elif s['format_bullet_text'] == '-':
                                new_export.bullets_type = 'CHARACTER_MINUS'
                            else:  # default
                                new_export.bullets_type = 'CHARACTER_STAR'
                    elif s['format_bullets_type'] == 'number':
                        if 'format_bullet_order' in s:
                            if s['format_bullet_order'] == 'desc':
                                new_export.bullets_type = 'NUMBER_DESC'
                            elif s['format_bullet_order'] == 'asc':
                                new_export.bullets_type = 'NUMBER_ASC'

            # links
            if 'link_has_detailed_record' in s and s['link_has_detailed_record']:
                new_export.show_detailed = True
            if 'link_has_fulltext' in s and s['link_has_fulltext']:
                new_export.show_fulltext = True
            if 'link_has_official' in s and s['link_has_official']:
                new_export.show_viewpublisher = True

            # divers
            if 'link_has_readable_links' in s and s['link_has_readable_links']:
                new_export.show_links_for_printing= True

            #TODO set the right user
            new_export.user = User.objects.all()[0]
            new_export.save()
            self.stdout.write("...saving {}".format(new_export.id))

        pdb.set_trace()
