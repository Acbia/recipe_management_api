from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Ingredient, Recipe
from .permissions import IsAdminForRecipeWrite


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True,
        allow_null=False,
    )
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
        required=True,
    )

    class Meta:
        model = Recipe
        fields = (
            "title",
            "description",
            "instructions",
            "category",
            "ingredients",
        )
        read_only_fields = ("user",)

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                "At least one ingredient is required."
            )
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.ingredients.set(ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if ingredients is not None:
            instance.ingredients.set(ingredients)

        return instance


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminForRecipeWrite]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminForRecipeWrite]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAdminForRecipeWrite]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path=r"category/(?P<category_id>\d+)")
    def by_category(self, request, category_id=None):
        queryset = self.get_queryset().filter(category_id=category_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"ingredient/(?P<ingredient_id>\d+)")
    def by_ingredient(self, request, ingredient_id=None):
        queryset = self.get_queryset().filter(ingredients__id=ingredient_id).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        title = (request.query_params.get("title") or "").strip()
        if not title:
            return Response(
                {"detail": "Query parameter 'title' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(title__icontains=title)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
