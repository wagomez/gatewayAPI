from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestFirstTest(APITestCase):
  """
  Verify WEB SERVER RESPONSE
  """
  def setUp(self):
      self.response = self.client.get('/')

  def test_received_200_status_code(self):
      self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class TestGetDevicesCMTS(APITestCase):
    """
    Verify GET CMTS DEVICES LODED ON NSO via Microservices API
    """
    def setUp(self):
        self.response = self.client.get('/getDevicesCMTS/')

    def test_GetCMTS_received_200_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_GetCMTS_infoRecived(self):
        info=self.response.content
        info=info.decode()
        print(info)
        busqueda=info.find('{"cmts":')
        if(busqueda<0):
            busqueda=True
        self.assertEqual(busqueda,True)


class TestGetDevicesPE(APITestCase):
    """
    Verify GET PE DEVICES LODED ON NSO via Microservices API
    """
    def setUp(self):
        self.response = self.client.get('/getDevicesPE/')

    def test_GetPE_received_200_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_GetPE_infoRecived(self):
        info=self.response.content
        info=info.decode()
        print(info)
        busqueda=info.find('{"pe":')
        if(busqueda<0):
            busqueda=True
        self.assertEqual(busqueda,True)



class TestSetLoadBalanceCMTS(APITestCase):
    """
    Verify Setting Load Balance to a CMTS via Microservices API
    """
    def setUp(self):
        self.response = self.client.get('/setLoadBalance/cbr8-1/0/0/')

    def test_GetCMTS_received_200_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


