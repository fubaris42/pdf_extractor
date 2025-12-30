# PDFExtractor

[ENGLISH LANGUAGE](./readme.en_us.md)

Aplikasi ekstraksi halaman PDF berperforma tinggi dengan **pencarian teks / regex**, **multi-proses**, **dukungan path panjang Windows**, serta **mode GUI dan CLI (gunakan core.py secara langsung)**.

PDFExtractor memindai file PDF di sebuah folder, mencari halaman yang mengandung pola tertentu, lalu **menyimpan hanya halaman yang cocok sebagai PDF baru**.

## Fitur

- Ekstrak halaman berdasarkan teks atau regex
- Mode regex atau teks biasa
- Multi-core processing
- Mendukung path Windows >260 karakter
- Struktur folder input tetap terjaga
- Binary mandiri (tanpa Python)

## Instalasi

### Binary Siap Pakai

1. Buka halaman **GitHub Releases**
2. Unduh file **ZIP**
3. Ekstrak
4. Jalankan:
   - `PDFExtractor.exe` (GUI) (buat desktop shortcut jika perlu)

### Compile sendiri

1. Windows

   ```powershell
   setup_and_build.ps1
   ```

2. Linux

   ```powershell
   setup_and_build.sh
   ```

## Cara Menggunakan

### GUI

1. Jalankan aplikasi
2. Masukkan pola pencarian atau upload file `.txt`
3. Pilih folder sumber PDF
4. Pilih folder output
5. Atur opsi (Regex, Case Sensitive, Recursive)
6. Klik **START EXTRACTION**
7. Log proses tampil langsung

### Pattern File (.txt) Format

1. Satu pola per baris
2. Baris kosong di abaikan

Contoh File.txt

```txt
foo
bar
baz
\bINV-\d{6}\b
```

## Regex Flavor

Menggunakan **Python `re` (standard library)**.

- Unicode aware
- Mendukung lookahead / lookbehind
- Word boundary `\b`
- Case-insensitive default

Jika **regex tidak aktif**, teks akan otomatis di-escape.

## Struktur Output

- Setiap halaman cocok → satu file PDF
- Struktur folder mengikuti input
- Nama file berisi:
  - Teks pertama yang cocok
  - Nama PDF asal
  - Nomor halaman

## Lisensi

beliin pilter sebungkus ama kopi segelas.
