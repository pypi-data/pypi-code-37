# coding: utf-8

"""
    Call Recorder API

    Call Recorder API   # noqa: E501

    OpenAPI spec version: 1.0.0
    
"""

from __future__ import absolute_import

import unittest

import call_recorder_api
from call_recorder_api.models.app import App
from call_recorder_api.models.device_type import DeviceType
from call_recorder_api.models.create_file_data import CreateFileData
from call_recorder_api.models.update_profile_request_data import UpdateProfileRequestData
from call_recorder_api.models.update_order_request import UpdateOrderRequest, FolderOrder
from call_recorder_api.rest import ApiException
from datetime import datetime

class TestContext:
    def __init__(self):
        self.token = '55942ee3894f51000530894'
        self.phone = '+16463742122'
        self.device_token = "871284c348e04a9cacab8aca6b2f3c9a"
        self.folder_pwd = "1234"
        self.code = None
        self.api_key = None
        self.created_file_id = None
        self.created_file_id2 = None
        self.created_folder_id = None
        self.created_folder_id2 = None
        self.created_meta_file_id = None

class TestApi(unittest.TestCase):
    """App unit test stubs"""

    ctx = None

    @classmethod
    def setUpClass(cls):
        cls.ctx = TestContext()

    def setUp(self):
        self.api = call_recorder_api.DefaultApi()
        self.ctx = TestApi.ctx

    def tearDown(self):
        pass

    def test1_RegisterPhone(self):
        """Test RegisterPhoneRequest"""
        
        res = self.api.register_phone_post(self.ctx.token, self.ctx.phone)

        self.assertEqual(res.status, 'ok')
        self.assertIsNotNone(res.code)
        self.assertGreater(len(res.code), 0)

        self.ctx.code = res.code

    def test2_VerifyPhone(self):
        """Test VerifyPhoneRequest"""
        
        res = self.api.verify_phone_post(
            token=self.ctx.token, 
            phone=self.ctx.phone, 
            code=self.ctx.code, 
            mcc='300', 
            app=App.REC, 
            device_type=DeviceType.IOS, 
            device_token=self.ctx.device_token, 
            device_id=self.ctx.device_token,
            time_zone=10
        )

        self.assertEqual(res.status, 'ok')
        self.assertEqual(res.phone, self.ctx.phone)
        self.assertGreater(len(res.api_key), 0)
        self.assertEqual(res.msg, "Phone Verified")

        self.ctx.api_key = res.api_key

    def test3_GetFiles(self):
        """Test GetFilesRequest"""

        res = self.api.get_files_post(
            api_key=self.ctx.api_key,
            page='0',
            folder_id=0,
            source='all',
            _pass='0',
            reminder=False,
            q='hello',
            id=0,
            op='less'
        )

        self.assertEqual(res.status, 'ok')
        self.assertEqual(res.credits, 0)
        self.assertEqual(res.credits_trans, 0)
        self.assertEqual(len(res.files), 0)

    def test4_CreateFile(self):
        """Test CreateFileRequest"""

        with open('test/resources/audio.mp3', 'rb') as f:
            res = self.api.create_file_post(
                api_key=self.ctx.api_key,
                file='test/resources/audio.mp3',
                data=CreateFileData(
                    name='test-file',
                    notes='test-notes',
                    remind_days='10',
                    remind_date=datetime.now()
                )
            )

            res2 = self.api.create_file_post(
                api_key=self.ctx.api_key,
                file='test/resources/audio.mp3',
                data=CreateFileData(
                    name='test-file2',
                    notes='test-notes',
                    remind_days='10',
                    remind_date=datetime.now()
                )
            )

            self.assertEqual(res.status, 'ok')
            self.assertTrue('successfully' in res.msg.lower())
            self.assertGreater(res.id, 0)

            self.ctx.created_file_id = res.id
            self.ctx.created_file_id2 = res2.id

    def test5_DeleteFiles(self):
        """Test DeleteFilesRequest"""

        res = self.api.delete_files_post(
            api_key=self.ctx.api_key,
            ids=[self.ctx.created_file_id],
            action='remove_forever'
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('successfully' in res.msg.lower())

    def test6_CreateFolder(self):
        """Test CreateFolderRequest"""
        
        res = self.api.create_folder_post(
            api_key=self.ctx.api_key,
            name='test-folder',
            _pass=self.ctx.folder_pwd
        )

        res2 = self.api.create_folder_post(
            api_key=self.ctx.api_key,
            name='test-folder2',
            _pass=self.ctx.folder_pwd
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('successfully' in res.msg.lower())
        self.assertIsNotNone(res.code)
        self.assertGreater(res.id, 0)

        self.ctx.created_folder_id = res.id
        self.ctx.created_folder_id2 = res2.id

    def test7_UpdateFolder(self):
        """Test UpdateFolderRequest"""
        
        res = self.api.update_folder_post(
            api_key=self.ctx.api_key,
            id=self.ctx.created_folder_id,
            name='test-folder-up',
            _pass=self.ctx.folder_pwd,
            is_private=False
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('folder update' in res.msg.lower())
        self.assertTrue(len(res.code))

    def test8_VerifyFolderPass(self):
        """Test VerifyFolderPassRequest"""
        
        res = self.api.verify_folder_pass_post(
            api_key=self.ctx.api_key,
            id=self.ctx.created_folder_id,
            _pass=self.ctx.folder_pwd
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('password is correct' in res.msg.lower())
        self.assertTrue(len(res.code))

    def test9_DeleteFolder(self):
        """Test DeleteFolderRequest"""
        
        res = self.api.delete_folder_post(
            api_key=self.ctx.api_key,
            id=self.ctx.created_folder_id,
            move_to=0
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())

    def test91_GetFolders(self):
        """Test GetFoldersRequest"""
        
        res = self.api.get_folders_post(
            api_key=self.ctx.api_key
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())
        self.assertGreater(len(res.folders), 0)
        for folder in res.folders:
            self.assertGreater(folder.id, 0)

    def test92_UpdateStar(self):
        """Test UpdateStarRequest"""
        
        res = self.api.update_star_post(
            api_key=self.ctx.api_key,
            id=self.ctx.created_file_id2,
            type='file',
            star=True
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())
        self.assertEqual(res.code, 'star_updated')

    def test93_CloneFile(self):
        """Test CloneFileRequest"""
        
        res = self.api.clone_file_post(
            api_key=self.ctx.api_key,
            id=self.ctx.created_file_id2
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())
        self.assertEqual(res.code, 'file_cloned')
        self.assertGreater(res.id, 0)

    def test94_UpdateProfileImg(self):
        """Test UpdateProfileImgRequest"""
        
        res = self.api.update_profile_img_post(
            api_key=self.ctx.api_key,
            file='test/resources/java.png'
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('profile picture updated' in res.msg.lower())
        self.assertEqual(res.code, 'profile_pic_updated')
        self.assertTrue(res.file.endswith('.png'))
        self.assertGreater(len(res.path), 0)

    def test95_UpdateProfile(self):
        """Test UpdateProfileRequest"""
        
        res = self.api.update_profile_post(
            api_key=self.ctx.api_key,
            data=UpdateProfileRequestData(
                f_name='testFName',
                l_name='testLName',
                email='test@mail.com',
                is_public=True,
                language='en_us'
            )
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('profile updated' in res.msg.lower())
        self.assertEqual(res.code, 'profile_updated')

    def test96_GetProfile(self):
        """Test GetProfileRequest"""
        
        res = self.api.get_profile_post(
            api_key=self.ctx.api_key
        )

        self.assertEqual(res.status, 'ok')
        self.assertEqual(res.code, 'user_profile')
        self.assertIsNotNone(res.profile)

    def test97_UpdateOrder(self):
        """Test UpdateOrderRequest"""
        
        res = self.api.update_order_post(
            api_key=self.ctx.api_key,
            folders=[
                FolderOrder(
                    id=self.ctx.created_folder_id2,
                    order_id=12345
                )
            ]
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('order updated' in res.msg.lower())
        self.assertEqual(res.code, 'order_updated')

    def test98_RecoverFile(self):
        """Test RecoverFileRequest"""
        
        res = self.api.recover_file_post(
            api_key=self.ctx.api_key,
            id=self.ctx.created_file_id,
            folder_id=self.ctx.created_folder_id2
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('successfully recovered' in res.msg.lower())
        self.assertEqual(res.code, 'file_recovered')
        
    def test99_UpdateSettings(self):
        """Test UpdateSettingsRequest"""
        
        res = self.api.update_settings_post(
            api_key=self.ctx.api_key,
            play_beep='no',
            files_permission='private'
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())
        self.assertEqual(res.code, 'settings_updated')
        
    def test991_GetSettings(self):
        """Test GetSettingsRequest"""
        
        res = self.api.get_settings_post(
            api_key=self.ctx.api_key
        )

        self.assertEqual(res.status, 'ok')
        self.assertGreater(len(res.app), 0)
        self.assertIsNotNone(res.credits)
        self.assertIsNotNone(res.credits)
        self.assertIsNotNone(res.settings.play_beep)
        self.assertIsNotNone(res.settings.files_permission)

    def test992_GetMessages(self):
        """Test GetMessagesRequest"""
        
        res = self.api.get_msgs_post(
            api_key=self.ctx.api_key
        )

        self.assertEqual(res.status, 'ok')
        self.assertGreater(len(res.msgs), 0)
        for msg in res.msgs:
            self.assertGreater(msg.id, 0)
            self.assertIsNotNone(msg.title)
            self.assertIsNotNone(msg.body)
            self.assertIsNotNone(msg.time)

    def test993_BuyCredits(self):
        """Test BuyCreditsRequest"""
        
        res = self.api.buy_credits_post(
            api_key=self.ctx.api_key,
            amount=100,
            receipt='test',
            device_type=DeviceType.IOS,
            product_id=1
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())

    def test994_UpdateDeviceToken(self):
        """Test UpdateDeviceTokenRequest"""
        
        res = self.api.update_device_token_post(
            api_key=self.ctx.api_key,
            device_token=self.ctx.device_token,
            device_type=DeviceType.IOS
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())

    def test995_GetTranslations(self):
        """Test GetTranslationsRequest"""
        
        res = self.api.get_translations_post(
            api_key=self.ctx.api_key,
            language='en_US'
        )

        self.assertEqual(res.status, 'ok')
        self.assertIsNotNone(res.translation)

    def test996_GetLanguages(self):
        """Test GetLanguagesRequest"""
        
        res = self.api.get_languages_post(
            api_key=self.ctx.api_key
        )

        self.assertEqual(res.status, 'ok')
        self.assertGreater(len(res.languages), 0)
        for lang in res.languages:
            self.assertIsNotNone(lang.code)
            self.assertIsNotNone(lang.name)

    def test997_GetPhones(self):
        """Test GetPhonesRequest"""
        
        res = self.api.get_phones_post(
            api_key=self.ctx.api_key
        )

        self.assertGreater(len(res), 0)
        for phone in res:
            self.assertIsNotNone(phone['phone_number'])
            self.assertIsNotNone(phone['number'])
            self.assertIsNotNone(phone['prefix'])
            self.assertIsNotNone(phone['friendly_name'])
            self.assertIsNotNone(phone['flag'])
            self.assertIsNotNone(phone['country'])
            #self.assertIsNotNone(phone['city'])

    def test998_UpdateUser(self):
        """Test UpdateUserRequest"""
        
        res = self.api.update_user_post(
            api_key=self.ctx.api_key,
            app=App.REC,
            timezone='10'
        )

        self.assertEqual(res.status, 'ok')

    def test999_NotifyUser(self):
        """Test NotifyUserRequest"""
        
        res = self.api.notify_user_post(
            api_key=self.ctx.api_key,
            title='test-title',
            body='test-body',
            device_type=DeviceType.IOS
        )

        self.assertEqual(res.status, 'ok')

    def test9991_UploadMetaFile(self):
        """Test UploadMetaFileRequest"""
        
        res = self.api.upload_meta_file_post(
            api_key=self.ctx.api_key,
            file='test/resources/java.png',
            name='test-meta',
            parent_id=self.ctx.created_file_id2,
            id=0
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())
        self.assertGreater(res.id, 0)
        self.assertEqual(res.parent_id, self.ctx.created_file_id2)

        self.created_meta_file_id = res.id

    def test9992_GetMetaFiles(self):
        """Test GetMetaFilesRequest"""
        
        res = self.api.get_meta_files_post(
            api_key=self.ctx.api_key,
            parent_id=self.ctx.created_file_id2
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue(len(res.meta_files) > 0)

    def test9993_DeleteMetaFiles(self):
        """Test DeleteMetaFilesRequest"""

        res = self.api.delete_meta_files_post(
            api_key=self.ctx.api_key,
            ids=[self.ctx.created_meta_file_id],
            parent_id=self.ctx.created_file_id2
        )

        self.assertEqual(res.status, 'ok')
        self.assertTrue('success' in res.msg.lower())


if __name__ == '__main__':
    unittest.main()
