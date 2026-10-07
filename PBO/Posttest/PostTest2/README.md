Sistem Pendataan dan Klasifikasi Kualitas Udara
Deskripsi Tema

Program ini mencatat data pengukuran kualitas udara dari beberapa stasiun pemantau, mengelola data tiap jenis polutan (PM2.5, PM10, CO, SO2, NO2, O3), lalu mengklasifikasikan hasilnya ke dalam kategori ISPU (Indeks Standar Pencemar Udara): Baik, Sedang, Tidak Sehat, Sangat Tidak Sehat, dan Berbahaya. Pada posttest ini ditambahkan class sensor yang menerapkan inheritance, serta relasi UML antar class berupa asosiasi, agregasi, dan komposisi.

Struktur Class

Program terdiri dari 7 class. Sensor adalah superclass, dengan dua subclass yaitu SensorPM dan SensorGas. StasiunPemantau menyimpan data satu stasiun pemantau (lokasi, kode, kode akses, ambang siaga) beserta daftar sensor yang terpasang. DataPolutan menyimpan data satu jenis polutan hasil pengukuran (jenis dan konsentrasi). DataUdara menggabungkan satu StasiunPemantau dengan sekumpulan DataPolutan pada satu waktu, beserta nilai ISPU. LaporanKualitas mengambil satu DataUdara dan mencetak laporan beserta klasifikasi kategori kualitas udara.

Relasi UML

Asosiasi: DataUdara merujuk ke StasiunPemantau lewat atribut stasiun, dan LaporanKualitas merujuk ke DataUdara lewat atribut dataUdara. Selain itu, method evaluasiSiaga(dataUdara) pada StasiunPemantau memakai objek DataUdara hanya sebagai parameter sementara dan tidak menyimpannya. Objek yang dirujuk tetap berdiri sendiri.

Agregasi: StasiunPemantau memiliki banyak Sensor lewat atribut _daftarSensor. Objek Sensor dibuat di luar stasiun, lalu dipasang lewat method tambahSensor(). Jika stasiun dihapus, objek sensor tetap ada dan bisa dipasang ke stasiun lain.

Komposisi: DataUdara memiliki banyak DataPolutan lewat atribut _daftarPolutan. Objek DataPolutan dibentuk langsung di dalam constructor DataUdara dari data mentah (dataPolutanAwal), sehingga data polutan menjadi bagian dari pengukuran tersebut dan tidak berdiri sendiri.

Inheritance

Superclass: Sensor. Subclass: SensorPM dan SensorGas. Kedua subclass memanggil constructor superclass memakai super().__init__(namaSensor, kodeSeri).

Atribut tambahan: SensorPM punya resolusiMikron, SensorGas punya jenisGas. Atribut ini membedakan tiap subclass dari parent maupun dari subclass lainnya.

Method overriding: method bacaData() pada Sensor membaca data secara generik. Method ini di-override pada SensorPM, yang menghitung nilai partikel dari resolusiMikron, dan pada SensorGas, yang membaca gas sesuai jenisGas.

Tingkat akses: atribut protected _statusAktif pada Sensor diakses langsung oleh kedua subclass di dalam bacaData() untuk memeriksa apakah sensor aktif. Atribut private __kodeSeri hanya milik Sensor dan tidak bisa diakses subclass, hanya bisa dilihat tersamar lewat method cekKodeSeri().

Rincian tiap class

Sensor punya atribut kelas totalSensor dan satuanDefault. Atribut publiknya namaSensor. Atribut protected-nya _statusAktif dan atribut privatnya __kodeSeri. Instance method-nya aktifkan(), matikan(), cekKodeSeri(), dan bacaData().

SensorPM adalah subclass dari Sensor dengan atribut tambahan resolusiMikron dan meng-override bacaData().

SensorGas adalah subclass dari Sensor dengan atribut tambahan jenisGas dan meng-override bacaData().

StasiunPemantau punya atribut kelas namaInstansi, totalStasiunTerdaftar, dan daftarKotaTerdaftar. Atribut publiknya kodeStasiun, namaLokasi, kota, dan ambangSiaga. Atribut protected-nya _daftarSensor. Atribut privatnya __kodeAkses, diakses lewat @property kodeAkses dan ditampilkan tersamar (masking). Instance method-nya tampilanInfo(), tambahSensor(), jalankanSemuaSensor(), dan evaluasiSiaga(dataUdara). Class method-nya dariDict() sebagai factory dan infoInstansi(). Static method-nya validasiKodeStasiun(), memvalidasi format HURUF-ANGKA seperti AWK-001.

DataPolutan punya atribut kelas jenisPolutanValid dan totalDataPolutan. Atribut publiknya jenis dan satuan. Atribut privatnya __konsentrasi, diakses lewat @property konsentrasi dan tidak boleh bernilai negatif. Instance method-nya tampilanInfo(). Class method-nya dariSensor() sebagai factory dari dict pembacaan sensor. Static method-nya isJenisValid().

DataUdara punya atribut kelas totalPengukuran dan MAKSPOLUTAN. Atribut publiknya stasiun dan waktuPengukuran. Atribut protected-nya _daftarPolutan. Atribut privatnya __nilaiIspu, diakses lewat @property nilaiIspu dan harus bernilai 0 sampai 500. Instance method-nya tambahPolutan() dan tampilanPengukuran(). Class method-nya buatCepat() sebagai factory dengan waktu otomatis. Static method-nya formatWaktuValid().

LaporanKualitas punya atribut kelas kategoriTerdaftar (daftar label kategori) dan totalLaporanDibuat. Atribut publiknya dataUdara dan judulLaporan. Atribut privatnya __catatanKhusus, diakses lewat @property catatanKhusus dan tidak boleh kosong. Instance method-nya cetakLaporan(). Class method-nya ringkasanSemuaLaporan(). Static method-nya klasifikasiIspu(), mengubah nilai ISPU menjadi label kategori memakai if/elif biasa.

Cara Menjalankan

Jalankan dengan perintah python3 main.py di terminal. Tidak ada dependency eksternal, hanya menggunakan modul standar datetime.

Panduan Pengujian

Bagian if __name__ == "__main__": di bawah kode program mendemonstrasikan seluruh fitur yang diminta. Untuk inheritance, program membuat dua objek SensorPM dan satu objek SensorGas, memasangnya ke stasiun (agregasi), lalu menjalankan jalankanSemuaSensor() sehingga bacaData() versi override tiap subclass terpanggil. Sensor yang dimatikan lewat matikan() diuji menolak membaca data, dan cekKodeSeri() menampilkan kode seri private secara tersamar. Total sensor ditampilkan dari atribut kelas totalSensor.

Untuk relasi UML, asosiasi diuji lewat evaluasiSiaga() yang menerima objek DataUdara sebagai parameter, agregasi lewat tambahSensor(), dan komposisi lewat pembuatan DataUdara dengan dataPolutanAwal sehingga objek DataPolutan terbentuk di dalamnya.

Semua instance method didemonstrasikan, yaitu tampilanInfo(), tampilanPengukuran(), tambahPolutan(), cetakLaporan(), dan evaluasiSiaga(). Semua class method juga didemonstrasikan, yaitu StasiunPemantau.dariDict(), infoInstansi(), DataPolutan.dariSensor(), DataUdara.buatCepat(), dan LaporanKualitas.ringkasanSemuaLaporan(). Semua static method didemonstrasikan juga, yaitu validasiKodeStasiun(), isJenisValid(), formatWaktuValid(), dan klasifikasiIspu().

Setter dan validasinya diuji dengan data valid maupun tidak valid. kodeAkses ditolak jika kurang dari 6 karakter. konsentrasi ditolak jika bernilai negatif. nilaiIspu ditolak jika di luar rentang 0 sampai 500. catatanKhusus ditolak jika kosong atau hanya berisi spasi. Setiap kasus tidak valid memunculkan ValueError yang ditangkap dengan try/except lalu dicetak pesan penolakannya. Batas MAKSPOLUTAN juga diuji dengan menambah polutan ke-6 ke udara1 untuk membuktikan batas slot bekerja.
