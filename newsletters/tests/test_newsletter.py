# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from django.db.utils import IntegrityError

from .factories import NewsletterFactory, GroupOfNewslettersFactory


class NewslettersTestCase(TestCase):
    def setUp(self):
        self.gon = GroupOfNewslettersFactory()

    def test_slug_is_unique_for_group_of_newsletters(self):
        nwsltr1 = NewsletterFactory(group_of_newsletters=self.gon)
        nwsltr1.save()
        with self.assertRaises(IntegrityError) as context:
            nwsltr2 = NewsletterFactory(
                group_of_newsletters=self.gon, slug=nwsltr1.slug
            )
            nwsltr2.save()

        self.assertTrue(
            "duplicate key value violates unique" in context.exception.args[0]
        )

    def test_same_slug_for_different_groups_of_newsletters(self):
        nwsltr1 = NewsletterFactory(group_of_newsletters=self.gon)
        nwsltr1.save()
        nwsltr2 = NewsletterFactory(
            group_of_newsletters=GroupOfNewslettersFactory(), slug=nwsltr1.slug
        )
        nwsltr2.save()

        self.assertEqual(nwsltr1.slug, nwsltr2.slug)
