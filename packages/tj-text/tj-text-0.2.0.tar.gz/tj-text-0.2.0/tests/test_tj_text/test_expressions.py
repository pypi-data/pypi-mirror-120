import pytest

from tj_text.typograph import ru_typus


class TestRuExpressions:
    """Tests for typograph.mixins.RuExpressions class."""

    @pytest.mark.parametrize(
        'word',
        ['без', 'перед', 'при', 'через', 'над', 'под', 'про', 'для', 'около', 'среди'],
    )
    def test_rep_positional_spaces_after_words(self, word):
        text = f'Неразрывный пробел после предлога {word} должен быть'
        result = ru_typus(text)

        assert result == f'Неразрывный пробел после предлога {word}\xa0должен быть'
