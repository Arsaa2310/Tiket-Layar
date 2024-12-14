from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Bioskop(models.Model):
    id_bioskop = models.AutoField(primary_key=True)
    nm_bioskop = models.CharField(max_length=25)
    alamat = models.CharField(max_length=100)
    kota = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nm_bioskop

class Teater(models.Model):
    id_teater = models.AutoField(primary_key=True)
    id_bioskop = models.ForeignKey(Bioskop, on_delete=models.CASCADE)
    nm_teater = models.CharField(max_length=20)
    kapasitas = models.SmallIntegerField()
    jenis_teater = models.IntegerField(null=True, blank=True)
    tipe_layar = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nm_teater

class Kursi(models.Model):
    id_kursi = models.AutoField(primary_key=True)
    id_teater = models.ForeignKey(Teater, on_delete=models.CASCADE, default=1) 
    baris_kursi = models.CharField(max_length=1)
    no_kursi = models.SmallIntegerField()
    status_kursi = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.baris_kursi}{self.no_kursi}"

class Pelanggan(AbstractUser):
    id_pelanggan = models.AutoField(primary_key=True)
    nm_pelanggan = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=5000)
    no_telepon = models.CharField(max_length=14)

    def __str__(self):
        return self.nm_pelanggan
    
# Model Film
class Film(models.Model):
    judul = models.CharField(max_length=100)
    durasi = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    sinopsis = models.TextField()
    rating = models.CharField(max_length=25)
    link_poster = models.CharField(max_length=500)

    def __str__(self):
        return self.judul

class Tiket(models.Model):
    id_tiket = models.AutoField(primary_key=True)
    id_kursi = models.ForeignKey(Kursi, on_delete=models.CASCADE)
    id_film = models.ForeignKey(Film, on_delete=models.CASCADE)
    kode_tiket = models.CharField(max_length=6, unique=True)
    tgl_film = models.DateField()
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    status_tiket = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.kode_tiket

class VirtualAccount(models.Model):
    id_va = models.AutoField(primary_key=True)
    no_va = models.IntegerField()
    nm_bank = models.IntegerField()

    def __str__(self):
        return str(self.no_va)

class Pembayaran(models.Model):
    id_pembayaran = models.AutoField(primary_key=True)
    id_tiket = models.ForeignKey(Tiket, on_delete=models.CASCADE)
    id_pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    id_va = models.ForeignKey(VirtualAccount, on_delete=models.CASCADE)
    kode_pembayaran = models.CharField(max_length=16)
    tgl_pembayaran = models.DateTimeField(auto_now_add=True)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status_pembayaran = models.IntegerField()

    def __str__(self):
        return self.kode_pembayaran