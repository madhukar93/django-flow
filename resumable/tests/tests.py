# -*- coding: utf-8 -*-
import os

from  urllib import urlencode

from django.conf import settings
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse

from resumable.files import ResumableFile


TESTS_ROOT = os.path.dirname(__file__)


seagull = {
    'resumableTotalSize': '147292',
    'resumableFilename': 'seagull.ogg',
    'resumableChunkNumber': '8',
}


craw = {
    'resumableTotalSize': '49028',
    'resumableFilename': 'craw.ogg',
    'resumableChunkNumber': '4',
}


class BaseTestCase(TestCase):
    def setUp(self):
        test_storage = FileSystemStorage(
            location=getattr(settings, 'FILE_UPLOAD_TEMP_DIR'))
        self.fixtures_root = os.path.join(TESTS_ROOT, 'fixtures', 'files',
            'chunks')
        fixtures_storage = FileSystemStorage(location=self.fixtures_root)

        for filename in fixtures_storage.listdir('.')[1]:
            test_storage.save(
                filename,
                fixtures_storage.open(filename)
            )
        self.seagull = ResumableFile(test_storage, seagull)
        self.craw = ResumableFile(test_storage, craw)
        self.storage = test_storage

    def tearDown(self):
        for filename in self.storage.listdir('.')[1]:
            self.storage.delete(filename)


class ResumableFileFieldTest(BaseTestCase):
    class ResumableForm():
        pass


class ResumableFileTest(BaseTestCase):
    def test_chunks(self):
        self.assertEqual(len(self.seagull.chunks), 7)

    def test_chunk_exists_existing(self):
        self.assertTrue(self.craw.chunk_exists)

    def test_chunk_exists_missing(self):
        self.assertFalse(self.seagull.chunk_exists)

    def test_file_complete(self):
        self.assertEqual(len(self.craw.file), 49028)

    def test_file_partial(self):
        self.assertRaises(lambda: self.seagull.file)

    def test_filename(self):
        self.assertEqual(self.seagull.filename, '147292_seagull.ogg')

    def test_is_complete_complete(self):
        self.assertTrue(self.craw.is_complete)

    def test_is_complete_partial(self):
        self.assertFalse(self.seagull.is_complete)

    def test_process_chunk(self):
        self.assertFalse(self.seagull.chunk_exists)
        self.seagull.process_chunk(ContentFile('content'))
        self.assertTrue(self.seagull.chunk_exists)

    def test_size_complete(self):
        self.assertEqual(self.craw.size, 49028)

    def test_size_partial(self):
        self.assertEqual(self.seagull.size, 71680)


class ResumableUploadViewTest(BaseTestCase):
    def test_get_existing(self):
        url = '%s?%s' % (reverse('upload'), urlencode(craw))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_get_missing(self):
        url = '%s?%s' % (reverse('upload'), urlencode(seagull))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)

    def test_post_missing(self):
        self.assertFalse(self.seagull.chunk_exists)
        params = dict(seagull, **{
            'file': open(os.path.join(self.fixtures_root, 'chunk'))
        })
        self.client.post(reverse('upload'), params)
        self.assertTrue(self.seagull.chunk_exists)
