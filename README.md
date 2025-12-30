# PDFExtractor

[ENGLISH LANGUAGE](./readme.en_us.md)

PDFExtractor adalah aplikasi untuk **memotong / mengekstrak halaman PDF secara otomatis** berdasarkan **kata kunci tertentu**.
Aplikasi ini sangat cocok untuk mengolah arsip PDF besar seperti invoice, laporan, kontrak, atau dokumen administrasi.

Aplikasi tersedia dalam bentuk **.exe (siap pakai)** dan **tidak memerlukan instalasi Python**.

---

## 🎯 Fungsi Utama

PDFExtractor akan melakukan hal berikut:

1. Membaca semua file PDF di sebuah folder
2. Mencari halaman yang mengandung **kata kunci tertentu**
3. Menyimpan **setiap halaman yang cocok** sebagai **file PDF baru**

📌 **Satu halaman yang cocok = satu file PDF hasil**

---

## ⭐ Keunggulan Aplikasi

* ✅ Pencarian berdasarkan **teks biasa atau regex**
* ✅ Bisa mencari **banyak kata sekaligus**
* ✅ Proses sangat cepat / 80% cpu core (multi-core CPU)
* ✅ Mendukung **Windows Long Path** (>260 karakter)
* ✅ Tampilan **GUI (klik-klik, tanpa terminal)**
* ✅ Struktur folder tetap rapi
* ✅ File hasil otomatis diberi nama jelas
* ✅ Siap pakai dalam bentuk **PDFExtractor.exe**

---

## 📥 Instalasi (Sangat Mudah)

### 1️⃣ Download Aplikasi

1. Buka halaman **GitHub Releases**
2. Download file **ZIP**
3. Klik kanan → **Extract All**

---

### 2️⃣ Buat Shortcut di Desktop (Disarankan)

1. Masuk ke folder hasil extract
2. Klik kanan pada `PDFExtractor.exe`
3. Pilih **Show More Options → Send to → Desktop (Create shortcut)**

Sekarang aplikasi bisa dibuka langsung dari Desktop.

---

## ▶️ Cara Menggunakan Aplikasi (GUI)

### Langkah Umum

1. Jalankan **PDFExtractor.exe**
2. Tentukan **Search Pattern**
3. Pilih **Source Folder** (folder berisi PDF)
4. Pilih **Output Folder**
5. Atur opsi pencarian jika perlu
6. Klik **START EXTRACTION**
7. Tunggu proses sampai selesai

Log proses akan tampil otomatis di bagian bawah aplikasi.

---

## 🔍 Cara Mengisi Kata Kunci (Search Pattern)

Ada **2 cara** memasukkan kata kunci:

---

### 🔹 Opsi 1 — Input Langsung (Satu Kata / Pola)

Gunakan cara ini jika hanya ingin mencari **satu kata atau satu pola**.

Contoh:

```
invoice
```

Atau pola khusus (regex):

```
\bINV-\d{6}\b
```

---

### 🔹 Opsi 2 — Menggunakan File `.txt` (Banyak Kata Sekaligus)

Gunakan cara ini jika ingin mencari **banyak kata sekaligus**.

#### Cara Membuat File `.txt`

1. Buka **Notepad**
2. Tulis **satu kata atau satu pola per baris**
3. Simpan sebagai file `.txt`
4. Klik tombol **Load .txt** di aplikasi

Contoh isi file:

```txt
invoice
total pembayaran
INV-2024
\bINV-\d{6}\b
```

📌 **Aturan penting**:

* Satu baris = satu kata / pola
* Baris kosong akan diabaikan

---

## ⚙️ Penjelasan Opsi

* **Regex**

  * Aktifkan jika menggunakan pola khusus (regex)
* **Case Sensitive**

  * Aktif jika ingin membedakan huruf besar dan kecil
* **Recursive**

  * Aktif jika ingin mencari PDF sampai ke subfolder

---

## 📁 Hasil Output

Setiap halaman yang cocok akan disimpan sebagai **file PDF baru** dengan format nama:

```
[KataKunci]_[NamaPDFAsal]_page_[NomorHalaman].pdf
```

Contoh:

```
INV-123456_LaporanKeuangan_page_7.pdf
```

📂 Struktur folder output akan **mengikuti struktur folder sumber**, sehingga tetap rapi dan mudah dicari.

---

## ⚠️ Peringatan Penting (WAJIB DIBACA)

### ❗ Jenis PDF yang Bisa Dibaca

Aplikasi ini **hanya bisa membaca PDF yang berisi teks digital**.

❌ **Tidak bisa diproses**:

* PDF hasil **foto HP**
* PDF hasil **scan dokumen**
* PDF yang teksnya **tidak bisa diblok / diseleksi**

Jika kamu membuka PDF dan **tidak bisa menyorot (block) teksnya**, maka:
➡️ **PDFExtractor tidak akan menemukan data apa pun**

✅ **Bisa diproses**:

* PDF dari Word / Excel
* PDF hasil export sistem
* PDF invoice, laporan, atau e-dokumen resmi

💡 **Solusi**:
Jika PDF kamu hasil scan, gunakan aplikasi **OCR (Optical Character Recognition)** terlebih dahulu.

---

### 🔐 PDF Ber-Password

* PDF yang **terenkripsi / memakai password** tidak bisa diproses
* Harus dibuka dan disimpan ulang tanpa password

---

### 💾 Ukuran File Sangat Besar

* PDF di atas **500MB – 1GB**:

  * Berisiko membuat aplikasi **crash**
  * Tergantung kapasitas RAM komputer

Ini adalah keterbatasan teknis dari:

* Library PDF (PyMuPDF)
* Memori sistem

💡 Tips:

* Pecah PDF besar sebelum diproses
* Tutup aplikasi berat lain saat menjalankan PDFExtractor

---

## 🧠 Tentang Regex (Singkat & Praktis)

PDFExtractor menggunakan **regex standar Python (`re`)**.

Regex cocok untuk:

* Nomor invoice
* Kode dokumen
* Pola teks konsisten

Contoh umum:

```
\bINV-\d{6}\b
```

Jika **Regex tidak dicentang**, aplikasi akan menganggap input sebagai **teks biasa**.

---

## 📜 Lisensi

Lisensi aplikasi ini sederhana dan jujur:

> **“Beliin rokok sebungkus ama kopi segelas.”**

☕🚬