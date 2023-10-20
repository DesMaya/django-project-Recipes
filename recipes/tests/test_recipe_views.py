from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve  # type: ignore
from recipes import views
# from unittest import skip


# Esse comando serve para pular o teste, seja todos os testes
# da classe ou apenas o teste em si que colocar o skip
# @skip("Estou pulando todos os testes para testar rs")


# Esse comando serve para forçar que o teste falhe
# e logo em seguida exiba a mensagem passada como
# parâmetro
# self.fail('')


class RecipeViewsTest(RecipeTestBase):

    # Esse método é executado sempre antes de qualquer
    # função dentro dessa classe
    def setUp(self) -> None:
        return super().setUp()

    # Esse método é executado sempre depois de qualquer
    # função dentro dessa classe
    def tearDown(self) -> None:
        return super().tearDown()

    # Home tests ---------------------------------------------------------

    def test_recipes_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_returns_status_code_200_ok(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertEqual(response.status_code, 200)

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_template_shows_no_recipes_found_if_no_recipes(self):
        # É possível deletar o model criado apenas para esse test
        # Recipe.objects.get(pk=1).delete()

        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertIn(
            "No Recipes!",
            response.content.decode(response.charset)
        )

    def test_recipes_home_template_loads_recipes(self):
        self.make_recipe(
            author_data={
                'first_name': 'Maya'
            },
            category_data={
                'name': 'Café da Manhã'
            },
            title='New Recipe Title',
            preparation_time=15
        )

        response = self.client.get(
            reverse('recipes:home'),
        )
        response_recipes = response.context['recipes']
        recipe = response_recipes.first()
        self.assertEqual(len(response_recipes), 1)
        self.assertEqual(recipe.title, 'New Recipe Title')

        content = response.content.decode(response.charset)
        self.assertIn('New Recipe Title', content)
        self.assertIn('15 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertIn('Café da Manhã', content)
        self.assertIn('Maya', content)

    # Category Tests ---------------------------------------------------------

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1}
            )
        )
        self.assertIs(view.func, views.category)

    def test_recipes_category_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1000}
            )
        )
        self.assertEqual(response.status_code, 404)

    # Detail Tests ---------------------------------------------------------

    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1}
            )
        )
        self.assertIs(view.func, views.recipes)

    def test_recipes_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1000}
            )
        )
        self.assertEqual(response.status_code, 404)
