# Generated by Django 3.2.18 on 2023-05-03 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('vote', models.CharField(choices=[('like', '<i class="far fa-laugh-squint EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i> 좋았다'), ('soso', '<i class="far fa-meh EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i>괜찮다'), ('dislike', '<i class="far fa-frown EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i>나쁘다')], max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='tourlist_destinations/')),
                ('category', models.CharField(choices=[('산', '산'), ('바다', '바다'), ('계곡', '계곡'), ('섬', '섬')], max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('price_range', models.CharField(max_length=20)),
                ('parking', models.BooleanField(default=False)),
                ('business_hours', models.CharField(max_length=50)),
                ('holiday', models.DateField()),
                ('website', models.URLField(blank=True, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('like_users', models.ManyToManyField(related_name='like_spots', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tourlist_destinations/')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='spots.comment')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spots.spot'),
        ),
        migrations.AddField(
            model_name='comment',
            name='like_users',
            field=models.ManyToManyField(related_name='like_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
