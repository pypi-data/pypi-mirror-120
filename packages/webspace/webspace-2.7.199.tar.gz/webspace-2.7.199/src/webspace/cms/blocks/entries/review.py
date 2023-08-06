from wagtail.core import blocks
from webspace.cms import constants
from wagtail.images.blocks import ImageChooserBlock
from webspace.cms.blocks.common import EntryBlock


class ReviewEntry(EntryBlock):
    testimonials = blocks.ListBlock(blocks.StructBlock([
        ('testimonial', blocks.TextBlock()),
        ('person_full_name', blocks.CharBlock()),
        ('person_title', blocks.CharBlock()),
        ('logo_company', ImageChooserBlock(required=False)),
        ('person_image', ImageChooserBlock(required=False)),
    ]))

    class Meta:
        template = '%s/entries/review.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Review"
        icon = 'grip'
