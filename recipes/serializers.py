from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(style={'base_template': 'textarea.html'})
    ingredients = serializers.CharField(style={'base_template': 'textarea.html'})
    url = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validated_data):
        """
        Create and return a new `Recipe` instance, given the validated data.
        """
        return Recipe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Recipe` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.ingredients = validated_data.get('ingredients', instance.ingredients)
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance