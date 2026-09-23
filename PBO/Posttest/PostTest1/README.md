Sistem Pendataan dan Klasifikasi Kualitas Udara
Deskripsi Tema

Program ini mencatat data pengukuran kualitas udara dari beberapa stasiun pemantau, mengelola data tiap jenis polutan (PM2.5, PM10, CO, SO2, NO2, O3), lalu mengklasifikasikan hasilnya ke dalam kategori ISPU (Indeks Standar Pencemar Udara): Baik, Sedang, Tidak Sehat, Sangat Tidak Sehat, dan Berbahaya.

Struktur Class

Program terdiri dari 4 class utama yang berdiri sendiri dan saling berinteraksi lewat objek, tanpa inheritance. StasiunPemantau menyimpan data satu stasiun pemantau (lokasi, kode, kode akses, ambang siaga). DataPolutan menyimpan data satu jenis polutan hasil pengukuran (jenis dan konsentrasi). DataUdara menggabungkan satu StasiunPemantau dengan sekumpulan DataPolutan pada satu waktu, beserta nilai ISPU. LaporanKualitas mengambil satu DataUdara dan mencetak laporan beserta klasifikasi kategori kualitas udara.

Rincian tiap class:

StasiunPemantau punya atribut kelas nama_instansi, total_stasiun_terdaftar, dan daftarKotaTerdaftar. Atribut publiknya kodeStasiun, namaLokasi, kota, dan ambangSiaga. Atribut privatnya __kodeAkses, diakses lewat @property kodeAkses dan ditampilkan tersamar (masking). Instance method-nya tampilkanInfo() dan evaluasiSiaga(dataUdara). Class method-nya dariDict() sebagai factory dan infoInstansi(). Static method-nya validasiKodeStasiun(), memvalidasi format HURUF-ANGKA seperti AWK-001.

DataPolutan punya atribut kelas jenisPolutanValid dan totalDataPolutan. Atribut publiknya jenis dan satuan. Atribut privatnya __konsentrasi, diakses lewat @property konsentrasi dan tidak boleh bernilai negatif. Instance method-nya tampilkanInfo(). Class method-nya dariSensor() sebagai factory dari dict pembacaan sensor. Static method-nya isJenisValid().

DataUdara punya atribut kelas totalPengukuran dan MAKSPOLUTAN. Atribut publiknya stasiun, waktuPengukuran, dan _daftarPolutan. Atribut privatnya __nilaiIspu, diakses lewat @property nilaiIspu dan harus bernilai 0 sampai 500. Instance method-nya tambahPolutan() dan tampilanPengukuran(). Class method-nya buatCepat() sebagai factory dengan waktu otomatis. Static method-nya formatWaktuValid().

LaporanKualitas punya atribut kelas kategoriTerdaftar (daftar label kategori) dan totalLaporanDibuat. Atribut publiknya dataUdara dan judulLaporan. Atribut privatnya __catatanKhusus, diakses lewat @property catatanKhusus dan tidak boleh kosong. Instance method-nya cetakLaporan(). Class method-nya ringkasanSemuaLaporan(). Static method-nya klasifikasiIspu(), mengubah nilai ISPU menjadi label kategori memakai if/elif biasa.

Cara Menjalankan

Jalankan dengan perintah python3 posttest1.py di terminal. Tidak ada dependency eksternal, hanya menggunakan modul standar datetime.

Panduan Pengujian

Bagian if __name__ == "__main__": di bawah kode program mendemonstrasikan seluruh fitur yang diminta. Program membuat minimal 2 objek untuk tiap class. Semua instance method didemonstrasikan, yaitu tampilkanInfo(), tampilkanPengukuran(), tambahPolutan(), cetakLaporan(), dan evaluasiSiaga(). Semua class method juga didemonstrasikan, yaitu StasiunPemantau.dariDict(), infoInstansi(), DataPolutan.dariSensor(), DataUdara.buatCepat(), dan LaporanKualitas.ringkasanSemuaLaporan(). Semua static method didemonstrasikan juga, yaitu validasiKodeStasiun(), isJenisValid(), formatWaktuValid(), dan klasifikasiIspu().

Setter dan validasinya diuji dengan data valid maupun tidak valid. kode_akses ditolak jika kurang dari 6 karakter. konsentrasi ditolak jika bernilai negatif. nilaiIspu ditolak jika di luar rentang 0 sampai 500. catatanKhusus ditolak jika kosong atau hanya berisi spasi. Setiap kasus tidak valid memunculkan ValueError yang ditangkap dengan try/except lalu dicetak pesan penolakannya. Batas MAKSPOLUTAN juga diuji dengan menambah polutan ke-6 ke udara1 untuk membuktikan batas slot bekerja