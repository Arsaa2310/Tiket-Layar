from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from .models import Pelanggan, Film, Bioskop, Teater, Tiket, Kursi

def home(request):
    return render(request, 'Layar_Tiket/home.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Pelanggan.objects.get(email=email)
                id_pelanggan = user.id_pelanggan
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('base',id_pelanggan = id_pelanggan)
                else:
                    form.add_error(None, "Invalid email or password")
            except Pelanggan.DoesNotExist:
                form.add_error(None, "User with this email does not exist")
    else:
        form = LoginForm()

    return render(request, 'Layar_Tiket/login.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'Layar_Tiket/signup.html', {'form': form})

def base(request, id_pelanggan):
    import re
    import requests
    from bs4 import BeautifulSoup
    def judul_rating(response):
        judul_movie = []
        rating_umr = []
        lis = response.find_all('div', {'class': 'movie-desc'})

        for i in lis:
            judul_movie.append(i.text[1:-2])
            try:
                rating_umr.append(i.find('img')['alt'])
            except:
                rating_umr.append('')

        return judul_movie, rating_umr

    def poster(response):
        link_poster = []
        lis = response.find_all('div', {'class': 'movie-poster'})

        for i in lis:
            link_poster.append(i.find('img')['src'])
        
        return link_poster

    def info_film(response):
        link_film = []
        lis = response.find_all('div',{'class':'movie'})

        for i in lis:
            try:
                link_film.append(i.find('a')['href'])
            except:
                link_film.append('')

        response = []
        for link in link_film:
            res = requests.get(link)
            res = BeautifulSoup(res.text,'html.parser')
            response.append(res)

        durasi = []
        genre = []
        sinopsis = []

        for i in response:
            # Mencari durasi    
            fil = i.find('div', {'class': 'c-duration cineplex'})
            durasi.append(fil.text if fil else '')

            # Mencari genre
            fil = i.find('li', {'class': 'movie_genre'})
            genre.append(fil.text[12:-9] if fil else '')

            # Mencari sinopsis
            fil = i.find('div', {'class': 'desc-synopsis'})
            sinopsis.append(fil.text[10:] if fil else '')

        sinopsis_cls = []
        for i in sinopsis:
            #sin = re.sub(r'\n','<br>',i)
            sin = re.sub(r'\r','',i)
            sinopsis_cls.append(sin)

        return sinopsis_cls, durasi, genre

    def update_data():
        res = requests.get('https://21cineplex.com')
        response = BeautifulSoup(res.text,'html.parser')
        Film.objects.all().delete()
        judul,rating = judul_rating(response)
        sinopsis, durasi, genre = info_film(response)
        link_poster = poster(response)    
        data_film = {
            'Judul': judul,
            'Durasi': durasi,
            'Gendre':genre,
            'Sinopsis': sinopsis,
            'Rating': rating,
            'Poster': link_poster
        }

        for i in range(len(data_film['Judul'])):
            Film.objects.create(
                judul = data_film['Judul'][i],
                durasi = data_film['Durasi'][i],
                genre = data_film['Gendre'][i],
                sinopsis = data_film['Sinopsis'][i],
                rating = data_film['Rating'][i],
                link_poster = data_film['Poster'][i]
            )

    update_data()
    data_film = Film.objects.all()
    data_film = [{"Judul": p.judul, "Poster": p.link_poster, "Rating": p.rating} for p in data_film]
    
    return render(request, 'Layar_Tiket/base.html', {'data': data_film})

def profil(request, id_pelanggan): 
    try:
        data_user = Pelanggan.objects.get(id_pelanggan=id_pelanggan)  
    except Film.DoesNotExist:
        data_user = None
    if data_user :
        data_user_data = {
        'Email': data_user.email,
        'Nama': data_user.nm_pelanggan,
        'ID' : data_user.id_pelanggan,
        }
    else:
        data_user_data = None
    return render(request, 'Layar_Tiket/profil.html', {'data': data_user_data})

def film(request, judul, id_pelanggan):
    # Memfilter film berdasarkan judul
    try:
        data_film = Film.objects.filter(judul=judul).first()
    except Film.DoesNotExist:
        data_film = None
    
    if data_film:
        data_film_data = {
            "Judul": data_film.judul,
            "Poster": data_film.link_poster,
            "Durasi": data_film.durasi,
            "Rating": data_film.rating,
            "Genre": data_film.genre,
            "Sinopsis": data_film.sinopsis, 
        }
    else:
        data_film_data = None

    return render(request, 'Layar_Tiket/film.html', {'movie': data_film_data})

def pesan_tiket(request, judul, id_pelanggan):
    try:
        data_film = Film.objects.filter(judul=judul).first()
        data_bioskop = Bioskop.objects.get(id_film = data_film.id_film)
        data_teater = Teater.objects.get()
    except Film.DoesNotExist:
        data_film = None

    if data_film and data_bioskop:
        data_film_data = {
            "Judul": data_film.judul,
            "Poster": data_film.link_poster,
            "Durasi": data_film.durasi,
            "Rating": data_film.rating,
            "Genre": data_film.genre,
            "Sinopsis": data_film.sinopsis, 
        }
        data_bioskop_data = {
            'Nama_Bioksop': data_bioskop.nm_bioskop,
            'Alamat_Bioskop': data_bioskop.alamat,
        }
        
    else:
        data_film_data = None
    print(data_bioskop)
    return render(request, 'Layar_Tiket/pesan.html')


    

    
