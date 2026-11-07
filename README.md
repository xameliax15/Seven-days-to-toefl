# Seven Days to TOEFL

![Ilustrasi utama Seven Days to TOEFL](gui/main_menu_toefl_library.png)

**Seven Days to TOEFL** adalah visual novel edukasi berbasis [Ren'Py](https://www.renpy.org/) yang mengajak pemain mempersiapkan TOEFL selama tujuh hari. Pemain mengikuti cerita sebuah kelompok belajar, mengerjakan latihan, membuat pilihan, dan menghadapi simulasi ujian pada hari terakhir.

## Informasi proyek

- Judul: Seven Days to TOEFL
- Versi: 1.0
- Engine: Ren'Py 8.5.2
- Bahasa: Indonesia
- Target skor dalam cerita: 400

## Fitur utama

- Cerita interaktif dengan pilihan pemain.
- Materi vocabulary, structure, reading, dan listening.
- Latihan serta evaluasi untuk setiap hari belajar.
- Kalender progres belajar selama tujuh hari.
- Simulasi TOEFL dan evaluasi akhir.
- Musik, efek suara, ilustrasi karakter, dan latar.
- Beberapa hasil akhir berdasarkan progres dan keputusan pemain.

## Menjalankan proyek

Repository ini berisi isi direktori `game` pada sebuah proyek Ren'Py.

1. Unduh dan pasang [Ren'Py SDK](https://www.renpy.org/latest.html).
2. Buat struktur direktori proyek berikut:

   ```text
   Seven Days to TOEFL/
   └── game/
   ```

3. Clone repository ini ke dalam direktori `game`:

   ```bash
   git clone https://github.com/xameliax15/Seven-days-to-toefl.git "Seven Days to TOEFL/game"
   ```

4. Letakkan direktori `Seven Days to TOEFL` di dalam direktori proyek Ren'Py.
5. Buka Ren'Py Launcher, pilih **Seven Days to TOEFL**, lalu tekan **Launch Project**.

## Struktur penting

```text
audio/       Musik, efek suara, dan audio soal listening
font/        Font yang digunakan oleh antarmuka
gui/         Aset antarmuka Ren'Py
images/      Karakter, latar, dan item permainan
script.rpy   Alur cerita dan logika utama
screens.rpy  Definisi layar dan komponen antarmuka
options.rpy  Konfigurasi proyek Ren'Py
gui.rpy      Konfigurasi tampilan
```

## Git LFS

File ZIP berukuran besar pada repository ini disimpan menggunakan [Git LFS](https://git-lfs.com/). Pastikan Git LFS sudah terpasang sebelum melakukan clone:

```bash
git lfs install
git clone https://github.com/xameliax15/Seven-days-to-toefl.git
```

## Pengembangan

Edit file `.rpy` menggunakan editor teks, kemudian jalankan ulang proyek dari Ren'Py Launcher untuk melihat perubahan. `config.autoreload` dinonaktifkan karena perubahan struktur dialog atau screen tidak selalu kompatibel dengan hot reload.

## Lisensi

Belum ada lisensi open-source yang ditetapkan. Seluruh hak atas kode dan aset tetap dimiliki oleh pemilik proyek.
