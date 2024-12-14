from django.contrib import admin
from .models import Film, Kursi, Tiket, Pembayaran, VirtualAccount, Teater, Bioskop, Pelanggan

# Daftarkan model di admin panel
admin.site.register(Film)
admin.site.register(Kursi)
admin.site.register(Tiket)
admin.site.register(Pembayaran)
admin.site.register(VirtualAccount)
admin.site.register(Teater)
admin.site.register(Bioskop)
admin.site.register(Pelanggan)
