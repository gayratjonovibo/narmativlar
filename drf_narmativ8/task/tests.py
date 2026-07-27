from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task
from .serializers import TaskSerializer

User = get_user_model()


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.task1 = Task.objects.create(
            title="Test Post 1",
            content="Test Content 1",
            author=self.user1
        )

        self.list_create_url = reverse('posts-list')  # ViewSet router nomi bo'yicha
        self.detail_url = reverse('posts-detail', kwargs={'pk': self.task1.pk})
        self.token_url = reverse('token_obtain_pair')


    def test_serializer_validation(self):
        data = {'title': 'New Task', 'content': 'Valid Content'}
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create_post_unauthenticated_fails(self):
        data = {'title': 'Unauthorized Post', 'content': 'No Token'}
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_permission_on_update(self):
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Hacked Title', 'content': 'Updated Content'}

        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_full_api_flow_integration(self):

        token_response = self.client.post(self.token_url, {
            'username': 'user1',
            'password': 'password123'
        })
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access_token = token_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        new_post_data = {'title': 'Integration Post', 'content': 'Integration Content'}
        create_response = self.client.post(self.list_create_url, new_post_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data['title'], 'Integration Post')

        get_response = self.client.get(self.list_create_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        created_post_id = create_response.data['id']
        update_url = reverse('posts-detail', kwargs={'pk': created_post_id})
        update_data = {'title': 'Updated Integration Post', 'content': 'Updated Content'}

        update_response = self.client.put(update_url, update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['title'], 'Updated Integration Post')