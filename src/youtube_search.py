import yt_dlp

def search_youtube(query):
    """
    Mencari video di YouTube berdasarkan query dan mengembalikan URL video paling atas.
    Args:
    - query: Kata kunci pencarian.
    Returns:
    - URL video paling atas (string) jika berhasil, None jika tidak ditemukan.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch',  # Menentukan pencarian YouTube
        'noplaylist': True,  # Hanya cari satu video, bukan playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
            # Cek apakah 'entries' ada dan memiliki hasil
            entries = info.get('entries')
            if entries:
                return entries[0]['webpage_url']  # URL video paling atas
            
            return None
    except yt_dlp.DownloadError as e:
        print(f"Error saat mendownload atau mencari video: {e}")
    except Exception as e:
        print(f"Error tidak terduga saat mencari video di YouTube: {e}")
    
    return None