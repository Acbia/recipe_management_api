from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")

urlpatterns = router.urls
