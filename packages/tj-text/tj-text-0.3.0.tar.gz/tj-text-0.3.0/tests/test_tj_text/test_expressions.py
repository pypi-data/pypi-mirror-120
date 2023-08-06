import pytest

from tj_text.typograph import ru_typus


class TestRuExpressions:
    """Tests for typograph.mixins.RuExpressions class."""

    @pytest.mark.parametrize(
        'word',
        ['без', 'перед', 'при', 'через', 'над', 'под', 'про', 'для', 'около', 'среди'],
    )
    def test_expr_rep_positional_spaces_after_long_preposiciones(self, word):
        text = f'Проверяем{word} предлог {word} неразрывным {word}пробелом {word}.'
        expected_result = (
            f'Проверяем{word} предлог {word}\xa0неразрывным {word}пробелом {word}.'
        )

        result = ru_typus(text)

        assert result == expected_result

    @pytest.mark.parametrize('word', ['же', 'ли', 'бы', 'б', 'уж'])
    def test_expr_rep_positional_spaces_before_particles(self, word):
        text = f'Проверяем{word} частицу {word} неразрывным {word}пробелом {word}.'
        expected_result = (
            f'Проверяем{word} частицу\xa0{word} неразрывным {word}пробелом\xa0{word}.'
        )

        result = ru_typus(text)

        assert result == expected_result
