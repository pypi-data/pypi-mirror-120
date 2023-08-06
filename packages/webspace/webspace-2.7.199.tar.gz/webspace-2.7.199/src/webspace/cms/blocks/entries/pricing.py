from wagtail.core import blocks
from webspace.cms import constants
from webspace.cms.blocks.common import \
    ButtonBlock, \
    EntryBlock


class PricingItem(blocks.StructBlock):
    header_title = blocks.CharBlock()
    header_description = blocks.TextBlock()
    price_month = blocks.DecimalBlock()
    price_unit = blocks.CharBlock(required=False)
    price_promotion = blocks.CharBlock(required=False)
    button = ButtonBlock()
    footer_title = blocks.CharBlock()
    features = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock()),
    ]))

    class Meta:
        template = '%s/entries/pricing_item.html' % constants.BLOCK_TEMPLATES_PATH


class PricingEntry(EntryBlock):
    card_1 = PricingItem()
    card_2 = PricingItem()
    card_3 = PricingItem()

    class Meta:
        template = '%s/entries/pricing.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Pricing"
        icon = 'grip'


class PricingDualEntry(EntryBlock):
    card_1 = PricingItem()
    card_2 = PricingItem()

    class Meta:
        template = '%s/entries/pricing_dual.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Pricing Dual"
        icon = 'grip'
