import pytest
from src.shared.domain.entities.category import Category
from src.shared.helpers.errors.domain_errors import EntityError

class Test_Category:
    def test_entity_correctly(self):
        category = Category(
            category_id='123',
            user_id='1',
            category_name='Jogos',
            category_primary_color='#721792',
            category_secondary_color='#FF0000'
        )

        assert type(category) == Category
        assert category.category_id == '123'
        assert category.user_id == '1'
        assert category.category_name == 'Jogos'
        assert category.category_primary_color == '#721792'
        assert category.category_secondary_color == '#FF0000'

    def test_entity_incorrectly_category_name(self):
        with pytest.raises(EntityError):
            Category(
                category_id='125',
                user_id='1',
                category_name='',
                category_primary_color='#721792',
                category_secondary_color='#FF0000'
            )
        with pytest.raises(EntityError):
            Category(
                category_id='127',
                user_id='1',
                category_name='a',
                category_primary_color='#721792',
                category_secondary_color='#FF0000'
            )
    
    def test_entity_incorrectly_category_primary_color(self):
        with pytest.raises(EntityError):
            Category(
                category_id='129',
                user_id='1',
                category_name='Jogos',
                category_primary_color='',
                category_secondary_color='#FF0000'
            )
        with pytest.raises(EntityError):
            Category(
                category_id='131',
                user_id='1',
                category_name='Jogos',
                category_primary_color='#FF',
                category_secondary_color='#FF0000'
            )
    
    def test_entity_incorrectly_category_secondary_color(self):
        with pytest.raises(EntityError):
            Category(
                category_id='133',
                user_id='1',
                category_name='Jogos',
                category_primary_color='#721792',
                category_secondary_color=''
            )
        with pytest.raises(EntityError):
            Category(
                category_id='135',
                user_id='1',
                category_name='Jogos',
                category_primary_color='#721792',
                category_secondary_color='#FF'
            )
