from abc import ABC, abstractmethod
from datetime import datetime

class Sensor(ABC):
    totalSensor = 0
    satuanDefault = "unit"

    def __init__(self, namaSensor, kodeSeri):
        self.namaSensor = namaSensor            # public
        self._statusAktif = True                # protected
        self.__kodeSeri = kodeSeri              # private
        Sensor.totalSensor += 1

    def __str__(self):
        status = "Aktif" if self._statusAktif else "Nonaktif"
        return f"Sensor {self.namaSensor} ({status})"

    def aktifkan(self):
        self._statusAktif = True

    def matikan(self):
        self._statusAktif = False

    def cekKodeSeri(self):
        return self.__kodeSeri[:3] + "***"

    @abstractmethod
    def bacaData(self):
        """Mengembalikan nilai hasil pembacaan sensor (angka)."""

    @abstractmethod
    def deskripsiPengukuran(self):
        """Mengembalikan teks singkat apa yang diukur sensor ini."""

    @abstractmethod
    def satuanUkur(self):
        """Mengembalikan satuan hasil pembacaan."""

    def jalankan(self):
        if not self._statusAktif:
            print(f"[{self.namaSensor}] Sensor nonaktif, tidak bisa membaca data.")
            return None
        nilai = self.bacaData()
        print(f"[{self.namaSensor}] {self.deskripsiPengukuran()}: {nilai} {self.satuanUkur()}")
        return nilai


class SensorPM(Sensor):
    def __init__(self, namaSensor, kodeSeri, resolusiMikron):
        super().__init__(namaSensor, kodeSeri)
        self.resolusiMikron = resolusiMikron

    def bacaData(self):
        return float(self.resolusiMikron * 10)

    def deskripsiPengukuran(self):
        return f"Partikel PM{self.resolusiMikron}"

    def satuanUkur(self):
        return "ug/m3"


class SensorGas(Sensor):
    def __init__(self, namaSensor, kodeSeri, jenisGas, nilaiSimulasi=0.0):
        super().__init__(namaSensor, kodeSeri)
        self.jenisGas = jenisGas
        self.nilaiSimulasi = nilaiSimulasi

    def bacaData(self):
        return float(self.nilaiSimulasi)

    def deskripsiPengukuran(self):
        return f"Gas {self.jenisGas}"

    def satuanUkur(self):
        return "ppm"


class SensorSuhu(Sensor):
    def __init__(self, namaSensor, kodeSeri, suhuCelsius):
        super().__init__(namaSensor, kodeSeri)
        self.suhuCelsius = suhuCelsius

    def bacaData(self):
        return float(self.suhuCelsius)

    def deskripsiPengukuran(self):
        return "Suhu udara sekitar"

    def satuanUkur(self):
        return "C"

class StasiunPemantau:
    namaInstansi = "Badan Pengendalian Lingkungan Ngawi"
    totalStasiunTerdaftar = 0
    daftarKotaTerdaftar = []

    def __init__(self, kodeStasiun, namaLokasi, kota, kodeAkses, ambangSiaga=300):
        self.kodeStasiun = kodeStasiun
        self.namaLokasi = namaLokasi
        self.kota = kota
        self.ambangSiaga = ambangSiaga
        self.__kodeAkses = None
        self.kodeAkses = kodeAkses
        self._daftarSensor = []

        StasiunPemantau.totalStasiunTerdaftar += 1
        if kota not in StasiunPemantau.daftarKotaTerdaftar:
            StasiunPemantau.daftarKotaTerdaftar.append(kota)

    def __str__(self):
        return f"Stasiun {self.kodeStasiun} ({self.namaLokasi}, {self.kota})"

    @property
    def kodeAkses(self):
        if self.__kodeAkses is None:
            return None
        return self.__kodeAkses[:2] + "*" * (len(self.__kodeAkses) - 2)

    @kodeAkses.setter
    def kodeAkses(self, value):
        if not isinstance(value, str) or len(value.strip()) < 6:
            raise ValueError("Kode akses minimal berisi 6 karakter dan tidak boleh kosong.")
        self.__kodeAkses = value.strip()

    def tampilanInfo(self):
        print(f"[Stasiun] {self}")
        print(f"    Kode Akses   : {self.kodeAkses}")
        print(f"    Ambang siaga : ISPU > {self.ambangSiaga}")
        print(f"    Sensor       : {len(self._daftarSensor)} terpasang")

    def tambahSensor(self, sensor):
        if not isinstance(sensor, Sensor):
            print(f"[{self.namaLokasi}] Bukan objek Sensor yang valid!")
            return
        self._daftarSensor.append(sensor)
        print(f"+ {sensor.namaSensor} terpasang di {self.namaLokasi}")

    def jalankanSemuaSensor(self):
        print(f"\n[{self.namaLokasi}] Menjalankan semua sensor:")
        for sensor in self._daftarSensor:
            sensor.jalankan()

    def evaluasiSiaga(self, dataUdara):
        if dataUdara.nilaiIspu > self.ambangSiaga:
            print(f"[{self.namaLokasi}] SIAGA! ISPU {dataUdara.nilaiIspu} "
                  f"melebihi ambang {self.ambangSiaga}.")
            return True
        print(f"[{self.namaLokasi}] Aman, ISPU {dataUdara.nilaiIspu} "
              f"masih di bawah ambang {self.ambangSiaga}.")
        return False

    @classmethod
    def dariDict(cls, data: dict):
        return cls(
            data["kodeStasiun"],
            data["namaLokasi"],
            data["kota"],
            data["kodeAkses"],
            data.get("ambangSiaga", 300),
        )

    @classmethod
    def infoInstansi(cls):
        print(f"Instansi Pengelola      : {cls.namaInstansi}")
        print(f"Total Stasiun Terdaftar : {cls.totalStasiunTerdaftar}")
        print(f"Kota Terpantau          : {', '.join(cls.daftarKotaTerdaftar)}")

    @staticmethod
    def validasiKodeStasiun(kode: str) -> bool:
        if not isinstance(kode, str) or "-" not in kode:
            return False
        bagian = kode.split("-")
        return len(bagian) == 2 and bagian[0].isalpha() and bagian[1].isdigit()


class DataPolutan:
    jenisPolutanValid = ["PM2.5", "PM10", "CO", "SO2", "NO2", "O3"]
    totalDataPolutan = 0

    def __init__(self, jenis, konsentrasi, satuan="ug/m3"):
        self.jenis = jenis
        self.satuan = satuan
        self.__konsentrasi = None
        self.konsentrasi = konsentrasi
        DataPolutan.totalDataPolutan += 1

    def __str__(self):
        return f"{self.jenis}: {self.konsentrasi} {self.satuan}"

    @property
    def konsentrasi(self):
        return self.__konsentrasi

    @konsentrasi.setter
    def konsentrasi(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Konsentrasi polutan tidak bisa negatif.")
        self.__konsentrasi = float(value)

    def tampilanInfo(self):
        print(f"    - {self}")

    @classmethod
    def dariSensor(cls, pembacaanSensor: dict):
        return cls(
            pembacaanSensor.get("jenis"),
            pembacaanSensor.get("nilai", 0),
            pembacaanSensor.get("satuan", "ug/m3"),
        )

    @staticmethod
    def isJenisValid(jenis: str) -> bool:
        return jenis in DataPolutan.jenisPolutanValid


class DataUdara:
    totalPengukuran = 0
    MAKSPOLUTAN = 5

    def __init__(self, stasiun, waktuPengukuran, nilaiIspu, dataPolutanAwal=None):
        self.stasiun = stasiun
        self.waktuPengukuran = waktuPengukuran
        self._daftarPolutan = []

        if dataPolutanAwal:
            self._daftarPolutan = [
                DataPolutan(jenis, nilai) for jenis, nilai in dataPolutanAwal
            ]
        self.__nilaiIspu = None
        self.nilaiIspu = nilaiIspu
        DataUdara.totalPengukuran += 1

    def __str__(self):
        return f"Pengukuran {self.stasiun.namaLokasi} @ {self.waktuPengukuran} (ISPU {self.nilaiIspu})"

    def __len__(self):
        return len(self._daftarPolutan)

    def __lt__(self, other):
        if not isinstance(other, DataUdara):
            return NotImplemented
        return self.nilaiIspu < other.nilaiIspu

    def __gt__(self, other):
        if not isinstance(other, DataUdara):
            return NotImplemented
        return self.nilaiIspu > other.nilaiIspu

    @property
    def nilaiIspu(self):
        return self.__nilaiIspu

    @nilaiIspu.setter
    def nilaiIspu(self, value):
        if not isinstance(value, (int, float)) or not (0 <= value <= 500):
            raise ValueError("Nilai ISPU harus berupa angka antara 0 dan 500.")
        self.__nilaiIspu = float(value)

    def tambahPolutan(self, jenis, konsentrasi):
        if len(self._daftarPolutan) >= DataUdara.MAKSPOLUTAN:
            print(f"Data polutan untuk {self.waktuPengukuran} sudah penuh, "
                  f"maksimal {DataUdara.MAKSPOLUTAN} jenis.")
            return
        self._daftarPolutan.append(DataPolutan(jenis, konsentrasi))

    def tampilanInfo(self):
        print(f"\n[pengukuran] {self}")
        for polutan in self._daftarPolutan:
            polutan.tampilanInfo()

    @classmethod
    def buatCepat(cls, stasiun, nilaiIspu):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        return cls(stasiun, waktu, nilaiIspu)

    @staticmethod
    def formatWaktuValid(waktuStr: str) -> bool:
        try:
            datetime.strptime(waktuStr, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False


class LaporanKualitas:
    kategoriTerdaftar = ["Baik", "Sedang", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"]
    totalLaporanDibuat = 0

    def __init__(self, dataUdara, judulLaporan):
        self.dataUdara = dataUdara
        self.judulLaporan = judulLaporan
        self.__catatanKhusus = ""
        self.catatanKhusus = "-"
        LaporanKualitas.totalLaporanDibuat += 1

    def __str__(self):
        return f"Laporan: {self.judulLaporan}"

    @property
    def catatanKhusus(self):
        return self.__catatanKhusus

    @catatanKhusus.setter
    def catatanKhusus(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Catatan tidak boleh kosong.")
        self.__catatanKhusus = value.strip()

    def cetakLaporan(self):
        kategori = LaporanKualitas.klasifikasiIspu(self.dataUdara.nilaiIspu)
        print(f"\n {self} ")
        self.dataUdara.tampilanInfo()
        print(f"    Kategori kualitas udara: {kategori}")
        print(f"    Catatan: {self.catatanKhusus}")

    @classmethod
    def ringkasanSemuaLaporan(cls):
        print(f"\nTotal laporan yang telah dibuat: {cls.totalLaporanDibuat}")

    @staticmethod
    def klasifikasiIspu(nilaiIspu: float) -> str:
        if nilaiIspu <= 50:
            return "Baik"
        elif nilaiIspu <= 100:
            return "Sedang"
        elif nilaiIspu <= 200:
            return "Tidak Sehat"
        elif nilaiIspu <= 300:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"

def tampilkanInfoSemua(daftarObjek):
    for objek in daftarObjek:
        objek.tampilanInfo()


def judul(teks):
    print("\n" + "=" * 60)
    print(teks)
    print("=" * 60)

#Testing Ground
if __name__ == "__main__":
    judul("SISTEM PENDATAAN DAN KLASIFIKASI KUALITAS UDARA")

    #1. Bukti abstraksi
    judul("1. ABSTRAKSI: abstract class tidak bisa diinstansiasi")
    try:
        sensorLangsung = Sensor("Sensor-Langsung", "SN-000")
    except TypeError as e:
        print(f"TypeError -> {e}")

    #2. Siapkan stasiun dan sensor
    judul("2. AGREGASI: sensor dibuat di luar, dipasang ke stasiun")
    stasiun1 = StasiunPemantau("AWK-001", "Jl. Sudirman", "Samarinda", "AKS12345", ambangSiaga=100)
    stasiun2 = StasiunPemantau.dariDict({
        "kodeStasiun": "AWK-002",
        "namaLokasi": "Jl. Gatot Subroto",
        "kota": "Balikpapan",
        "kodeAkses": "AKS67890",
        "ambangSiaga": 150,
    })

    sensorPm1 = SensorPM("Sensor-PM-01", "SN-PM-001", 2.5)
    sensorPm2 = SensorPM("Sensor-PM-02", "SN-PM-002", 10)
    sensorGas1 = SensorGas("Sensor-Gas-01", "SN-GS-001", "CO", nilaiSimulasi=8.2)
    sensorSuhu1 = SensorSuhu("Sensor-Suhu-01", "SN-SH-001", 31.5)

    for sensor in (sensorPm1, sensorPm2, sensorGas1, sensorSuhu1):
        stasiun1.tambahSensor(sensor)

    # ---------- 3. Polimorfisme via pewarisan
    judul("3. POLIMORFISME PEWARISAN satu loop, perilaku bacaData() berbeda")
    daftarSensor = [sensorPm1, sensorPm2, sensorGas1, sensorSuhu1]
    for sensor in daftarSensor:
        sensor.jalankan()

    print("\nLewat method stasiun (loop di dalam StasiunPemantau):")
    stasiun1.jalankanSemuaSensor()

    print("\nSensor dimatikan, lalu dijalankan lagi:")
    sensorGas1.matikan()
    sensorGas1.jalankan()
    sensorGas1.aktifkan()
    print(f"Total sensor terdaftar: {Sensor.totalSensor}")
    print(f"Kode seri tersamar {sensorPm2.namaSensor}: {sensorPm2.cekKodeSeri()}")

    #4. Data udara (komposisi)
    judul("4. KOMPOSISI: DataPolutan dibuat di dalam DataUdara")
    udara1 = DataUdara(
        stasiun1, "2026-10-20 08:00", 42,
        dataPolutanAwal=[("PM2.5", 50.0), ("CO", 8.2)],
    )
    udara1.tambahPolutan("O3", 20.0)
    udara1.tambahPolutan("NO2", 15.0)
    udara1.tambahPolutan("SO2", 5.0)
    print("Uji batas MAKSPOLUTAN (polutan ke-6, harus ditolak):")
    udara1.tambahPolutan("PM10", 30.0)

    udara2 = DataUdara.buatCepat(stasiun2, 155)
    udara2.tambahPolutan("SO2", 12.0)

    udara3 = DataUdara(stasiun1, "2026-10-20 14:00", 120, dataPolutanAwal=[("PM10", 95.0)])

    #5. Duck typing
    judul("5. DUCK TYPING: satu fungsi, kelas tidak berelasi pewarisan")
    polutanContoh = DataPolutan.dariSensor({"jenis": "CO", "nilai": 8.2, "satuan": "ppm"})
    tampilkanInfoSemua([stasiun1, polutanContoh, udara2])

    #6. Operator overloading
    judul("6. OPERATOR OVERLOADING: __len__, __lt__, __gt__, __str__")
    print(f"len(udara1)  = {len(udara1)} jenis polutan")
    print(f"len(udara2)  = {len(udara2)} jenis polutan")
    print(f"udara1 < udara2 ? {udara1 < udara2}  (ISPU {udara1.nilaiIspu} vs {udara2.nilaiIspu})")
    print(f"udara1 > udara2 ? {udara1 > udara2}")
    print("\nDiurutkan dari ISPU terendah (sorted() memakai __lt__):")
    for u in sorted([udara2, udara3, udara1]):
        print(f"  {u}")
    print(f"\nPengukuran terburuk (max() memakai __gt__/__lt__): {max([udara1, udara2, udara3])}")

    #7. Asosiasi + laporan
    judul("7. ASOSIASI: evaluasi siaga & laporan")
    stasiun1.evaluasiSiaga(udara1)
    stasiun2.evaluasiSiaga(udara2)

    laporan1 = LaporanKualitas(udara1, "Laporan Harian Samarinda")
    laporan1.catatanKhusus = "Kondisi normal, tidak ada anomali sensor."
    laporan2 = LaporanKualitas(udara2, "Laporan Harian Balikpapan")
    laporan1.cetakLaporan()
    laporan2.cetakLaporan()
    LaporanKualitas.ringkasanSemuaLaporan()

    # 8. Validasi
    judul("8. VALIDASI SETTER (data tidak valid ditolak)")
    for deskripsi, aksi in [
        ("kodeAkses 'abc'", lambda: setattr(stasiun1, "kodeAkses", "abc")),
        ("nilaiIspu 600", lambda: setattr(udara1, "nilaiIspu", 600)),
        ("catatanKhusus kosong", lambda: setattr(laporan2, "catatanKhusus", "   ")),
    ]:
        try:
            aksi()
        except ValueError as e:
            print(f"  {deskripsi} ditolak -> {e}")
