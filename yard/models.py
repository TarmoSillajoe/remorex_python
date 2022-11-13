from django.db import models


class Car(models.Model):
    model = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.model}, {self.description}"


class CarInstance(models.Model):
    model = models.ForeignKey(Car, on_delete=models.CASCADE)
    vin = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return f"{self.registration_number} {self.model.model}"


class AssemblyGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Part(models.Model):
    part_code = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", null=True)
    cars = models.ManyToManyField(Car)
    assembly_group = models.ForeignKey(
        AssemblyGroup, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.part_code}, {self.description}"
