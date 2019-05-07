# Generated by Django 2.2.1 on 2019-05-07 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rankings.fields
import rankings.models.ballot


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('politico_uid', models.SlugField(max_length=500, unique=True)),
                ('fec_candidate_id', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('complete', models.BooleanField(default=False)),
                ('note', rankings.fields.MarkdownField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.PositiveSmallIntegerField(blank=True, null=True, validators=[rankings.models.ballot.validate_rank])),
                ('note', models.TextField(blank=True, null=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ballots', related_query_name='ballot', to='rankings.Candidate')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballots', related_query_name='ballot', to='rankings.Poll')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ballots', related_query_name='ballot', to='rankings.Voter')),
            ],
            options={
                'unique_together': {('poll', 'voter', 'candidate'), ('poll', 'voter', 'ranking')},
            },
        ),
        migrations.CreateModel(
            name='AdminBallot',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Admin ballots',
                'ordering': ('poll', 'voter', 'ranking'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rankings.ballot',),
        ),
        migrations.CreateModel(
            name='UserBallot',
            fields=[
            ],
            options={
                'verbose_name_plural': 'My ballots',
                'ordering': ('ranking', 'candidate__name'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rankings.ballot',),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.PositiveSmallIntegerField()),
                ('points', models.PositiveSmallIntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rankings', related_query_name='ranking', to='rankings.Candidate')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rankings', related_query_name='ranking', to='rankings.Poll')),
            ],
            options={
                'ordering': ('-poll', 'ranking'),
                'unique_together': {('poll', 'candidate'), ('poll', 'ranking')},
            },
        ),
        migrations.CreateModel(
            name='CandidateNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', rankings.fields.MarkdownField(blank=True, null=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidate_notes', related_query_name='candidate_note', to='rankings.Candidate')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='candidate_notes', related_query_name='candidate_note', to='rankings.Poll')),
            ],
            options={
                'unique_together': {('poll', 'candidate')},
            },
        ),
    ]
