from webspace.cms import constants
from webspace.cms.blocks.common import \
    EntryBlock, \
    AccordionBlock


class AccordionEntry(EntryBlock):
    amp_scripts = ['accordion']
    items = AccordionBlock()

    def mock(self, *args, **kwargs):
        classic = {
            'type': 'classic',
            'value': {
                'head': {'value': self.p},
                'content': {'value': self.p},
            }
        }

        self.mock_data.update({
            'type': 'accordion',
            'value': {
                'items': [classic, classic, classic, classic]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/accordion.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Accordion"
        icon = 'list-ul'
