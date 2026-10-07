from datetime import datetime

class Sensor:
    totalSensor = 0
    satuanDefault = "unit"

    def __init__(self, namaSensor, kodeSeri):
        self.namaSensor = namaSensor
        self._statusAktif = True
        self.__kodeSeri = kodeSeri
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

    def bacaData(self):
        if not self._statusAktif:
            print(f"[{self.namaSensor}] Sensor nonaktif, tidak bisa membaca data.")
            return None
        print(f"[{self.namaSensor}] Membaca data generik...")
        return 0


class SensorPM(Sensor):
    def __init__(self, namaSensor, kodeSeri, resolusiMikron):
        super().__init__(namaSensor, kodeSeri)
        self.resolusiMikron = resolusiMikron

    def bacaData(self):
        if not self._statusAktif:
            print(f"[{self.namaSensor}] Sensor nonaktif, tidak bisa membaca data.")
            return None
        nilai = self.resolusiMikron * 10
        print(f"[{self.namaSensor}] Membaca partikel PM{self.resolusiMikron}: {nilai} ug/m3")
        return nilai


class SensorGas(Sensor):
    def __init__(self, namaSensor, kodeSeri, jenisGas):
        super().__init__(namaSensor, kodeSeri)
        self.jenisGas = jenisGas

    def bacaData(self):
        if not self._statusAktif:
            print(f"[{self.namaSensor}] Sensor nonaktif, tidak bisa membaca data.")
            return None
        print(f"[{self.namaSensor}] Membaca gas {self.jenisGas}...")
        return self.jenisGas


class StasiunPemantau:
    namaInstansi = "Badan Pengendalian Lingkungan Ngawi"
    totalStasiunTerdaftar = 0
    daftarKotaTerdaftar = []

    def __init__(self, kodeStasiun, namaLokasi, kota, kodeAkses, ambangSiaga = 300):
        self.kodeStasiun = kodeStasiun
        self.namaLokasi = namaLokasi
        self.kota = kota
        self.kodeAkses = kodeAkses
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
            raise ValueError(
                "Kode akses minimal berisi 6 karakter dan tidak boleh kosong (* ￣︿￣)"
            )
        self.__kodeAkses = value.strip()
        #instance meth
    def tampilanInfo(self):
        print(f"[Stasiun] {self}")
        print(f"    Kode Akses: {self.kodeAkses}")
        print(f"    Ambang siaga ISPU   :{self.ambangSiaga}")

    #Agregasi: objek Sensor dibuat di luar, baru ditempel ke stasiun lewat method ini
    def tambahSensor(self, sensor):
        if not isinstance(sensor, Sensor):
            print(f"[{self.namaLokasi}] Bukan objek Sensor yang valid!")
            return
        self._daftarSensor.append(sensor)
        print(f"+ {sensor.namaSensor} terpasang di {self.namaLokasi}")

    def jalankanSemuaSensor(self):
        print(f"\n[{self.namaLokasi}] Menjalankan semua sensor:")
        for sensor in self._daftarSensor:
            sensor.bacaData()

    #Asosiasi: dataUdara cuma dipakai sementara sebagai parameter, tidak disimpan permanen
    def evaluasiSiaga(self, dataUdara):
        if dataUdara.nilaiIspu > self.ambangSiaga:
            print(f"[{self.namaLokasi}] SIAGA! SIAGA TEOOOOOOT ISPU ISPU {dataUdara.nilaiIspu}"
                  f"Melebihi ambang {self.ambangSiaga}")
            return True
        print(f"[{self.namaLokasi}] Amamn, ISPU {dataUdara.nilaiIspu}"
              f"Masih dibawah ambang {self.ambangSiaga}")
        return False

    #classMethod
    @classmethod
    def dariDict(cls, data: dict):
        return cls(
            data["kodeStasiun"],
            data["namaLokasi"],
            data["kota"],
            data["kodeAkses"],
            data.get("ambangSiaga", 300)
        )
    @classmethod
    def infoInstansi(cls):
        print(f"Instansi Pengelola      : {cls.namaInstansi}")
        print(f"Total Stasiun Terdaftar : {cls.totalStasiunTerdaftar}")
        print(f"Kota Terpantau          : {', '.join(cls.daftarKotaTerdaftar)}")

    #StaticMethid
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
        #Public att
        self.jenis = jenis
        self.satuan = satuan
        #Priv att
        self.__konsentrasi = None
        self.konsentrasi = konsentrasi
        DataPolutan.totalDataPolutan += 1

    def __str__(self):
        return f"{self.jenis}: {self.konsentrasi} {self.satuan}"
    #Prop
    @property
    def konsentrasi(self):
        return self.__konsentrasi

    @konsentrasi.setter
    def konsentrasi(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Konsentrasi polutan tidak bisa negatif.")
        self.__konsentrasi = float(value)
    #instance method
    def tampilanInfo(self):
        print(f"    - {self}")
    #Class Method
    @classmethod
    def dariSensor(cls, pembacaanSensor: dict):
        return cls(
            pembacaanSensor.get("jenis"),
            pembacaanSensor.get("nilai", 0),
            pembacaanSensor.get("satuan", "ug/m3")
        )
    #Static Method
    @staticmethod
    def isJenisValid(jenis: str) -> bool:
        return jenis in DataPolutan.jenisPolutanValid
class DataUdara:
    #class att
    totalPengukuran = 0
    MAKSPOLUTAN = 5

    def __init__(self, stasiun, waktuPengukuran, nilaiIspu, dataPolutanAwal = None):
        #instance Pub att
        self.stasiun = stasiun
        self.waktuPengukuran = waktuPengukuran
        self._daftarPolutan = []

        #Komposisi: DataPolutan dibentuk langsung di dalam DataUdara dari data mentah
        if dataPolutanAwal:
            self._daftarPolutan = [
                DataPolutan(jenis, nilai) for jenis, nilai in dataPolutanAwal
            ]
        #Priv Inst att
        self.__nilaiIspu = None
        self.nilaiIspu = nilaiIspu
        DataUdara.totalPengukuran += 1
    def __str__(self):
        return f"Pengukuran {self.stasiun.namaLokasi} @ {self.waktuPengukuran} (ISPU {self.nilaiIspu})"

    #Prop
    @property
    def nilaiIspu(self):
        return self.__nilaiIspu
    @nilaiIspu.setter
    def nilaiIspu(self, value):
        if not isinstance(value, (int, float)) or not (0 <= value <= 500):
            raise ValueError("Nilai ISPU harus berupa angkat antara 0 dan 500.")
        self.__nilaiIspu = float(value)

    #Instance method
    def tambahPolutan(self, dataPolutan):
        #Agregasi: DataPolutan dibuat di luar, baru ditempel lewat method ini
        if len(self._daftarPolutan) >= DataUdara.MAKSPOLUTAN:
            print(f"Data polutan buat {self.waktuPengukuran} udah penuh, "
                  f"maksimal {DataUdara.MAKSPOLUTAN} jenis.")
            return
        self._daftarPolutan.append(dataPolutan)
    def tampilanPengukuran(self):
        print(f"\n[pengukuran] {self}")
        for polutan in self._daftarPolutan:
            polutan.tampilanInfo()
    @classmethod
    #mau buat namanya instant report nanti malah jadi jaksel
    def buatCepat(cls, stasiun, nilaiIspu):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        return cls(stasiun, waktu, nilaiIspu)
    #Static MEthod
    @staticmethod
    def formatWaktuValid(waktuStr : str) -> bool:
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
        return f"Laporan:   {self.judulLaporan}"

    @property
    def catatanKhusus(self):
        return self.__catatanKhusus

    @catatanKhusus.setter
    def catatanKhusus(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Catatan tidak dibenarkan kosong.")
        self.__catatanKhusus = value.strip()

    def cetakLaporan(self):
        kategori = LaporanKualitas.klasifikasiIspu(self.dataUdara.nilaiIspu)
        print(f"\n {self} ")
        self.dataUdara.tampilanPengukuran()
        print(f"    Kategori kualitas udara: {kategori}")
        print(f"    Catatan: {self.catatanKhusus}")

    @classmethod
    def ringkasanSemuaLaporan(cls):
        print(f"\nTotal laporan yang telah dibuat:  {cls.totalLaporanDibuat}")

    @staticmethod
    def klasifikasiIspu(nilaiIspu: float) -> str:
        if nilaiIspu <= 50:
            return "Baik"
        elif nilaiIspu <= 100:
            return "Sedang"
        elif nilaiIspu <= 199:
            return "Tidak Sehat"
        elif nilaiIspu <= 299:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"

#Testing Ground

if __name__ == "__main__":
    print("=" * 60)
    print("SISTEM PENDATAAN DAN KLASIFIKASI KUALITAS UDARA")
    print("=" * 60)

    print("\nUji Class: StasiunPemantau")
    stasiun1 = StasiunPemantau("AWK-001", "Jl. Sudirman", "Samarinda", "AKS12345", ambangSiaga=100)
    stasiun2 = StasiunPemantau.dariDict({
        "kodeStasiun": "AWK-002",
        "namaLokasi": "Jl. Gatot Subroto",
        "kota": "Balikpapan",
        "kodeAkses": "AKS67890",
        "ambangSiaga": 150,
    })
    stasiun1.tampilanInfo()
    stasiun2.tampilanInfo()
    StasiunPemantau.infoInstansi()

    print("\nValidasi format kode stasiun (staticmethod):")
    print(f"  'AWK-001' valid? {StasiunPemantau.validasiKodeStasiun('AWK-001')}")
    print(f"  'AWK001'  valid? {StasiunPemantau.validasiKodeStasiun('AWK001')}")

    print("\nUji setter KodeAkses dengan data nonvalid:")
    try:
        stasiun1.kodeAkses = "abc"
    except ValueError as e:
        print(f"    Ditolak -> {e}")

    #Uji sensor + inheritance
    print("\nUji Class: Sensor, SensorPM, SensorGas (inheritance)")
    sensorPm1 = SensorPM("Sensor-PM-01", "SN-PM-001", 2.5)
    sensorPm2 = SensorPM("Sensor-PM-02", "SN-PM-002", 10)
    sensorGas1 = SensorGas("Sensor-Gas-01", "SN-GS-001", "CO")

    stasiun1.tambahSensor(sensorPm1)
    stasiun1.tambahSensor(sensorGas1)
    stasiun1.jalankanSemuaSensor()

    print(f"\nTotal sensor terdaftar (class attribute): {Sensor.totalSensor}")
    print(f"Kode seri tersamar {sensorPm2.namaSensor}: {sensorPm2.cekKodeSeri()}")

    print("\nUji sensor nonaktif:")
    sensorGas1.matikan()
    sensorGas1.bacaData()
    sensorGas1.aktifkan()

    #Uji POlutan
    print("\nUji Class: DataPolutan")
    polutan1 = DataPolutan("PM2.5", 45.5)
    polutan2 = DataPolutan.dariSensor({"jenis": "CO", "nilai": 8.2, "satuan": "ppm"})
    polutan1.tampilanInfo()
    polutan2.tampilanInfo()

    print(f"\nTotal data polutan tercatat: {DataPolutan.totalDataPolutan}")
    print(f"Apakah 'PM10' jenis valid? {DataPolutan.isJenisValid('PM10')}")
    print(f"Apakah 'Debu' jenis valid? {DataPolutan.isJenisValid('Debu')}")

    print("\nUji setter konsentrasi dengan data TIDAK VALID:")
    try:
        polutan1.konsentrasi = -10
    except ValueError as e:
        print(f"  Ditolak -> {e}")

    print("Uji setter konsentrasi dengan data VALID:")
    polutan1.konsentrasi = 50.0
    print(f"  Konsentrasi baru PM2.5: {polutan1.konsentrasi}")

    #Uji dataUDara
    print("\nUji Class DataUdara")
    udara1 = DataUdara(
        stasiun1, "2026-09-23 08:00", 42,
        dataPolutanAwal=[("PM2.5", 50.0), ("CO", 8.2)],
    )
    udara1.tambahPolutan(DataPolutan("O3", 20.0))
    udara1.tambahPolutan(DataPolutan("NO2", 15.0))
    udara1.tambahPolutan(DataPolutan("SO2", 5.0))
    print("\nUji batas MAKSPOLUTAN (nambah polutan ke-6, harus ditolak):")
    udara1.tambahPolutan(DataPolutan("PM10", 30.0))

    udara2 = DataUdara.buatCepat(stasiun2, 155)
    udara2.tambahPolutan(DataPolutan("SO2", 12.0))

    udara1.tampilanPengukuran()
    udara2.tampilanPengukuran()

    print(f"\nTotal pengukuran tercatat: {DataUdara.totalPengukuran}")
    print(f"Format '2026-09-23 08:00' valid? {DataUdara.formatWaktuValid('2026-09-23 08:00')}")
    print(f"Format '23-09-2026' valid?       {DataUdara.formatWaktuValid('23-09-2026')}")

    print("\nUji setter nilaiIspu dengan data TIDAK VALID:")
    try:
        udara1.nilaiIspu = 600
    except ValueError as e:
        print(f"  Ditolak -> {e}")

    print("\nEvaluasi siaga (asosiasi)")
    stasiun1.evaluasiSiaga(udara1)
    stasiun2.evaluasiSiaga(udara2)

    #Uji laporan kualitas
    print("\nUji Class LaporanKualitas")
    laporan1 = LaporanKualitas(udara1, "Laporan Harian Samarinda")
    laporan1.catatanKhusus = "Kondisi normal, tidak ada anomali sensor."
    laporan2 = LaporanKualitas(udara2, "Laporan Harian Balikpapan")

    laporan1.cetakLaporan()
    laporan2.cetakLaporan()

    LaporanKualitas.ringkasanSemuaLaporan()

    print("\nUji setter catatanKhusus dengan data TIDAK VALID (kosong):")
    try:
        laporan2.catatanKhusus = "   "
    except ValueError as e:
        print(f"  Ditolak -> {e}")
