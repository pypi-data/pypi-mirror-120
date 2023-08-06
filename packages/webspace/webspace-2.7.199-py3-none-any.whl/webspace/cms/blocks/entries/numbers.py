from webspace.cms import constants
from webspace.cms.blocks.common import \
    NumbersBlock, \
    EntryBlock


class NumbersEntry(EntryBlock):
    items = NumbersBlock()

    def mock(self, *args, **kwargs):
        classic = {
            'type': 'classic',
            'value': {
                'number': 90,
                'unit': '%',
                'content': {'value': self.p},
            }
        }

        self.mock_data.update({
            'type': 'numbers',
            'value': {
                'items': [classic, classic, classic, classic]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/numbers.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Numbers"
        icon = 'grip'
