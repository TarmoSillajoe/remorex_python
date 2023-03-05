from django.test import TestCase
from yard.models import Car, CarInstance


class CarTestCase(TestCase):
    def createCar(self, model="test_model", description="test_description"):
        return Car.objects.create(model=model, description=description)

    def test_car_creation(self):
        car = self.createCar()
        self.assertTrue(isinstance(car, Car))
        self.assertEqual(car.__str__(), f"{car.model}, {car.description}")
