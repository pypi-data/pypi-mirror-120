# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-02-17 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statistics", "0010_auto_20190304_1747"),
    ]

    operations = [
        migrations.AddField(
            model_name="componentexecutedata",
            name="version",
            field=models.CharField(default="legacy", max_length=255, verbose_name="插件版本"),
        ),
        migrations.AddField(
            model_name="componentintemplate",
            name="version",
            field=models.CharField(default="legacy", max_length=255, verbose_name="插件版本"),
        ),
        migrations.AlterField(
            model_name="componentexecutedata",
            name="subprocess_stack",
            field=models.TextField(default="[]", help_text="JSON 格式的列表", verbose_name="子流程堆栈"),
        ),
        migrations.AlterField(
            model_name="componentintemplate",
            name="subprocess_stack",
            field=models.TextField(default="[]", help_text="JSON 格式的列表", verbose_name="子流程堆栈"),
        ),
    ]
