Sistem Pendataan dan Klasifikasi Kualitas Udara
Deskripsi Tema

Program ini mencatat data pengukuran kualitas udara dari beberapa stasiun pemantau, mengelola data tiap jenis polutan (PM2.5, PM10, CO, SO2, NO2, O3), lalu mengklasifikasikan hasilnya ke dalam kategori ISPU (Indeks Standar Pencemar Udara): Baik, Sedang, Tidak Sehat, Sangat Tidak Sehat, dan Berbahaya. Pada posttest ini class Sensor diubah menjadi abstract class, ditambahkan subclass SensorSuhu, serta diterapkan polimorfisme berupa pewarisan, duck typing, dan operator overloading.

Struktur Class

Program terdiri dari 8 class. Sensor adalah abstract class (superclass), dengan tiga subclass yaitu SensorPM, SensorGas, dan SensorSuhu. StasiunPemantau menyimpan data satu stasiun pemantau (lokasi, kode, kode akses, ambang siaga) beserta daftar sensor yang terpasang. DataPolutan menyimpan data satu jenis polutan hasil pengukuran (jenis dan konsentrasi). DataUdara menggabungkan satu StasiunPemantau dengan sekumpulan DataPolutan pada satu waktu, beserta nilai ISPU. LaporanKualitas mengambil satu DataUdara dan mencetak laporan beserta klasifikasi kategori kualitas udara.

Class Diagram

![Class Diagram](images/class_diagram.png)

Relasi UML

Asosiasi: DataUdara merujuk ke StasiunPemantau lewat atribut stasiun, dan LaporanKualitas merujuk ke DataUdara lewat atribut dataUdara. Selain itu, method evaluasiSiaga(dataUdara) pada StasiunPemantau memakai objek DataUdara hanya sebagai parameter sementara dan tidak menyimpannya. Objek yang dirujuk tetap berdiri sendiri.

Agregasi: StasiunPemantau memiliki banyak Sensor lewat atribut _daftarSensor. Objek Sensor dibuat di luar stasiun, lalu dipasang lewat method tambahSensor(). Jika stasiun dihapus, objek sensor tetap ada dan bisa dipasang ke stasiun lain.

Komposisi: DataUdara memiliki banyak DataPolutan lewat atribut _daftarPolutan. Objek DataPolutan dibentuk langsung di dalam DataUdara, baik lewat constructor dari data mentah (dataPolutanAwal) maupun lewat method tambahPolutan(jenis, konsentrasi), sehingga data polutan menjadi bagian dari pengukuran tersebut dan tidak berdiri sendiri.

Abstraksi

Abstract class: Sensor, dibuat dengan mewarisi ABC sehingga tidak bisa diinstansiasi langsung. Abstract method ada tiga dan ditandai @abstractmethod, yaitu bacaData(), deskripsiPengukuran(), dan satuanUkur().

Subclass SensorPM, SensorGas, dan SensorSuhu mengimplementasikan ketiga abstract method tersebut.

Method konkret: jalankan() pada Sensor dipakai bersama oleh semua subclass. Method ini memeriksa _statusAktif, memanggil bacaData() milik subclass, lalu mencetak hasilnya memakai deskripsiPengukuran() dan satuanUkur().

Inheritance dari posttest sebelumnya tetap dipakai: setiap subclass memanggil super().__init__(namaSensor, kodeSeri). Atribut tambahan: SensorPM punya resolusiMikron, SensorGas punya jenisGas dan nilaiSimulasi, SensorSuhu punya suhuCelsius. Atribut protected _statusAktif diakses subclass lewat jalankan() milik Sensor, sedangkan atribut private __kodeSeri hanya milik Sensor dan hanya bisa dilihat tersamar lewat method cekKodeSeri().

Bukti abstract class tidak bisa diinstansiasi: program mencoba membuat Sensor("Sensor-Langsung", "SN-000") di dalam try/except, lalu TypeError yang muncul dicetak. Hasilnya ada pada screenshot output.

Polimorfisme

Polimorfisme via pewarisan: method bacaData() di-override oleh SensorPM (nilai dari resolusi partikel), SensorGas (nilai simulasi gas), dan SensorSuhu (suhu udara) dengan perilaku berbeda. Ketiganya dipanggil lewat satu loop pada objek Sensor yang berbeda-beda, yaitu for sensor in daftarSensor: sensor.jalankan() di bagian utama program dan jalankanSemuaSensor() pada StasiunPemantau.

Duck typing: StasiunPemantau, DataPolutan, dan DataUdara tidak berhubungan lewat pewarisan, tetapi sama-sama punya method tampilanInfo(). Ketiganya dipanggil lewat satu fungsi yang sama, yaitu tampilkanInfoSemua(daftarObjek).

Operator overloading: DataUdara mendefinisikan __len__ (jumlah jenis polutan), __lt__ dan __gt__ (membandingkan nilai ISPU, dipakai oleh sorted() dan max()), serta __str__. Class lain juga memakai __str__.

Larangan anti-pattern: tidak ada rantai if/elif yang memeriksa type() atau string jenis objek. Perbedaan perilaku sensor ditentukan oleh method tiap subclass. klasifikasiIspu() memakai if/elif hanya pada angka ambang batas ISPU, bukan pada jenis objek. Satu-satunya isinstance ada di tambahSensor() dan hanya dipakai untuk validasi parameter.

Rincian tiap class

Sensor punya atribut kelas totalSensor dan satuanDefault. Atribut publiknya namaSensor. Atribut protected-nya _statusAktif dan atribut privatnya __kodeSeri. Instance method-nya aktifkan(), matikan(), cekKodeSeri(), dan jalankan(). Abstract method-nya bacaData(), deskripsiPengukuran(), dan satuanUkur().

SensorPM adalah subclass dari Sensor dengan atribut tambahan resolusiMikron dan meng-override ketiga abstract method.

SensorGas adalah subclass dari Sensor dengan atribut tambahan jenisGas dan nilaiSimulasi, serta meng-override ketiga abstract method.

SensorSuhu adalah subclass dari Sensor dengan atribut tambahan suhuCelsius dan meng-override ketiga abstract method.

StasiunPemantau punya atribut kelas namaInstansi, totalStasiunTerdaftar, dan daftarKotaTerdaftar. Atribut publiknya kodeStasiun, namaLokasi, kota, dan ambangSiaga. Atribut protected-nya _daftarSensor. Atribut privatnya __kodeAkses, diakses lewat @property kodeAkses dan ditampilkan tersamar (masking). Instance method-nya tampilanInfo(), tambahSensor(), jalankanSemuaSensor(), dan evaluasiSiaga(dataUdara). Class method-nya dariDict() sebagai factory dan infoInstansi(). Static method-nya validasiKodeStasiun(), memvalidasi format HURUF-ANGKA seperti AWK-001.

DataPolutan punya atribut kelas jenisPolutanValid dan totalDataPolutan. Atribut publiknya jenis dan satuan. Atribut privatnya __konsentrasi, diakses lewat @property konsentrasi dan tidak boleh bernilai negatif. Instance method-nya tampilanInfo(). Class method-nya dariSensor() sebagai factory dari dict pembacaan sensor. Static method-nya isJenisValid().

DataUdara punya atribut kelas totalPengukuran dan MAKSPOLUTAN. Atribut publiknya stasiun dan waktuPengukuran. Atribut protected-nya _daftarPolutan. Atribut privatnya __nilaiIspu, diakses lewat @property nilaiIspu dan harus bernilai 0 sampai 500. Instance method-nya tambahPolutan(jenis, konsentrasi) dan tampilanInfo(). Magic method-nya __str__, __len__, __lt__, dan __gt__. Class method-nya buatCepat() sebagai factory dengan waktu otomatis. Static method-nya formatWaktuValid().

LaporanKualitas punya atribut kelas kategoriTerdaftar (daftar label kategori) dan totalLaporanDibuat. Atribut publiknya dataUdara dan judulLaporan. Atribut privatnya __catatanKhusus, diakses lewat @property catatanKhusus dan tidak boleh kosong. Instance method-nya cetakLaporan(). Class method-nya ringkasanSemuaLaporan(). Static method-nya klasifikasiIspu(), mengubah nilai ISPU menjadi label kategori memakai if/elif pada angka ambang batas.

Cara Menjalankan

Jalankan dengan perintah python3 posttest3.py di terminal. Tidak ada dependency eksternal, hanya menggunakan modul standar abc dan datetime.

Panduan Pengujian

Bagian if __name__ == "__main__": di bawah kode program mendemonstrasikan seluruh fitur yang diminta, dibagi menjadi 8 bagian bertajuk. Bagian 1 membuktikan abstraksi: Sensor dicoba diinstansiasi dan TypeError ditangkap lalu dicetak. Bagian 2 membuat dua stasiun, dua objek SensorPM, satu SensorGas, dan satu SensorSuhu, lalu memasangnya ke stasiun lewat tambahSensor() (agregasi).

Bagian 3 menguji polimorfisme pewarisan: satu loop memanggil jalankan() pada semua sensor, lalu jalankanSemuaSensor() pada stasiun. Sensor yang dimatikan lewat matikan() diuji menolak membaca data, dan cekKodeSeri() menampilkan kode seri private secara tersamar. Total sensor ditampilkan dari atribut kelas totalSensor.

Bagian 4 menguji komposisi lewat pembuatan DataUdara dengan dataPolutanAwal dan tambahPolutan(), termasuk batas MAKSPOLUTAN dengan menambah polutan ke-6 ke udara1 untuk membuktikan batas slot bekerja. Bagian 5 menguji duck typing lewat tampilkanInfoSemua() yang menerima StasiunPemantau, DataPolutan, dan DataUdara. Bagian 6 menguji operator overloading: len(), perbandingan < dan >, sorted(), dan max() pada objek DataUdara.

Bagian 7 menguji asosiasi lewat evaluasiSiaga() yang menerima objek DataUdara sebagai parameter, lalu membuat dan mencetak LaporanKualitas. Semua class method didemonstrasikan, yaitu StasiunPemantau.dariDict(), infoInstansi(), DataPolutan.dariSensor(), DataUdara.buatCepat(), dan LaporanKualitas.ringkasanSemuaLaporan(). Semua static method didemonstrasikan juga, yaitu validasiKodeStasiun(), isJenisValid(), formatWaktuValid(), dan klasifikasiIspu().

Bagian 8 menguji setter dan validasinya dengan data tidak valid. kodeAkses ditolak jika kurang dari 6 karakter. konsentrasi ditolak jika bernilai negatif. nilaiIspu ditolak jika di luar rentang 0 sampai 500. catatanKhusus ditolak jika kosong atau hanya berisi spasi. Setiap kasus tidak valid memunculkan ValueError yang ditangkap dengan try/except lalu dicetak pesan penolakannya.

Screenshot Output Program

Bukti abstract class tidak bisa diinstansiasi

![Output abstraksi](images/output_1_abstraksi.png)

Polimorfisme pewarisan dan agregasi

![Output polimorfisme](images/output_2_polimorfisme.png)

Komposisi, duck typing, dan operator overloading

![Output duck typing dan operator overloading](images/output_3_duck_operator.png)

Asosiasi, laporan, dan validasi

![Output laporan](images/output_4_laporan.png)

Nilai Plus: Prinsip SOLID

Open/Closed Principle (OCP): class SensorSuhu ditambahkan sebagai subclass baru tanpa mengubah satu baris pun di Sensor maupun StasiunPemantau. Stasiun langsung bisa memasang dan menjalankan sensor jenis baru karena jalankanSemuaSensor() hanya memanggil jalankan() milik abstraksi Sensor.

Dependency Inversion Principle (DIP): StasiunPemantau bergantung pada abstraksi Sensor, bukan pada class konkret SensorPM, SensorGas, atau SensorSuhu. Hal ini terlihat pada tambahSensor(sensor) yang menerima objek bertipe Sensor dan menjalankannya lewat method abstrak.
