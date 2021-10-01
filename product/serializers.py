from rest_framework import serializers

from .models import Post, Comment, Rating, Favourite


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'user', 'body', 'publish', 'image', 'avr_rating')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        return rep


class PostDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['like'] = instance.likes.count()
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        if request.user.is_anonymous:
            raise serializers.ValidationError('Добавлят могут только авторизованные!!!')
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'text', 'user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class RatingSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'rate', 'post', 'user', )

    def validate(self, attrs):
        post = attrs.get('post')
        request = self.context.get('request')
        user = request.user
        if Rating.objects.filter(post=post, user=user).exists():
            raise serializers.ValidationError('Невозможно рейтинг ставить дважды')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class FavouritePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('post', 'id')

        def get_favourite(self, obj, request):
            if obj.favourite and request.user and request.user == obj.user:
                return obj.favourite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favourite'] = self.get_favourite(instance)
            return rep
