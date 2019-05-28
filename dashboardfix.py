from multiprocessing import Process, Pipe
from random import randint, uniform
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import time
from functools import partial as part
#from PySide import QtGui, QtCore

class utsv2:

    kecepatan = 0
    root = ''
    jarakTempuh = 0
    labelJarakTempuh = ''
    labelKecepatan = ''
    labelJarakDepan = ''
    labelJarakBelakang = ''
    labelJarakKanan = ''
    labelJarakKiri = ''
    labelTraffic = ''
    labelDepanKanan = ''
    labelDepanKiri = ''
    labelTindakan = ''
    path = ['Terus', 'Terus', 'Belok Kiri', 'Terus', 'Belok Kanan', 'Terus', 'Belok Kanan']
    patIndex = 0
	
		
    def kirimDepan(self, depan):
        while True:
            jarakDepan = randint(300, 500)
            # print("Jarak depan: ", jarakDepan)
            depan.send({'jarak': jarakDepan, 'dari': 'depan'})
            depan.close

    def kirimDepanKiri(self, depanKiri):
        while True:
            jarakDepanKiri = randint(200, 400)
            # print("Jarak depan kiri: ", jarakDepanKiri)
            depanKiri.send({'jarak': jarakDepanKiri, 'dari': 'depan_kiri'})
            depanKiri.close

    def kirimDepanKanan(self, depanKanan):
        while True:
            jarakDepanKanan = randint(200, 400)
            # print("Jarak depan kanan: ", jarakDepanKanan)
            depanKanan.send({'jarak': jarakDepanKanan, 'dari': 'depan_kanan'})
            depanKanan.close

    def kirimBelakang(self, belakang):
        while True:
            jarakBelakang = randint(200, 400)
            # print("Jarak belakang: ", jarakBelakang)
            belakang.send({'jarak': jarakBelakang, 'dari': 'belakang'})
            belakang.close

    def kirimKanan(self, kanan):
        while True:
            jarakKanan = randint(0, 100)
            # print("Jarak samping kanan: ", jarakKanan)
            kanan.send({'jarak': jarakKanan, 'dari': 'kanan'})
            kanan.close

    def kirimKiri(self, kiri):
        while True:
            jarakKiri = randint(0, 100)
            # print("Jarak samping kiri: ", jarakKiri)
            kiri.send({'jarak': jarakKiri, 'dari': 'kiri'})
            kiri.close

    def kirimTraffic(self, traffic):
        while True:
            jarakTraffic = randint(0, 500)
            # print("Jarak traffic: ", jarakTraffic)
            warnaLampu = {1: 'Merah', 2: 'Kuning', 3: 'Hijau'}
            indexWarnaLampu = randint(1, 3)
            traffic.send({'jarak': jarakTraffic, 'dari': 'traffic', 'warnaLampu': warnaLampu[indexWarnaLampu]})
            traffic.close

    def berhenti(self):
        time.sleep(5)

    def masterControl(self, depan, belakang, depanKanan, depanKiri, kanan, kiri, traffic):
        if self.jarakTempuh <= 3000000:
            dataDepan = depan.recv()
            dataBelakang = belakang.recv()
            dataDepanKanan = depanKanan.recv()
            dataDepanKiri = depanKiri.recv()
            dataKanan = kanan.recv()
            dataKiri = kiri.recv()
            dataTraffic = traffic.recv()
            jarakDepan = dataDepan['jarak']
            jarakBelakang = dataBelakang['jarak']
            jarakDepanKanan = dataDepanKanan['jarak']
            jarakDepanKiri = dataDepanKiri['jarak']
            jarakKanan = dataKanan['jarak']
            jarakKiri = dataKiri['jarak']
            jarakTraffic = dataTraffic['jarak']
            warnaLampu = dataTraffic['warnaLampu']
            labelJarakDepan.config(text="Jarak depan: "+str(jarakDepan)+"Meter")
            labelJarakBelakang.config(text="Jarak belakang: "+str(jarakBelakang)+"Meter")
            labelDepanKanan.config(text="Jarak depan kanan: "+str(jarakDepanKanan)+"Meter")
            labelDepanKiri.config(text="Jarak depan kiri: "+str(jarakDepanKiri)+"Meter")
            labelJarakKanan.config(text="Jarak kanan: "+str(jarakKanan)+"Meter")
            labelJarakKiri.config(text="Jarak kiri: "+str(jarakKiri)+"Meter")
            labelTraffic.config(text="Jarak traffic: "+str(jarakTraffic))

            if jarakDepan < 400: # jarak aman 4m / 400cm
                labelTindakan.config(text="Rem depan")
            elif jarakKanan < 30: # jarak aman 30cm
                labelTindakan.config(text="Geser kiri")
            elif jarakKiri < 20: # jarak aman 20cm
                labelTindakan.config(text="Geser kanan")
            elif jarakBelakang < 300: # jarak aman 3m / 300cm
                labelTindakan.config(text="Jalan")
            elif warnaLampu == 'Merah':
                labelTindakan.config(text="Lampu merah Berhenti")
                self.berhenti()
                labelTindakan.config(text=self.path[self.patIndex])
                self.patIndex += 1
            elif warnaLampu == 'Kuning':
                labelTindakan.config(text="Lampu kuning")
            else:
                labelTindakan.config(text="Jalan")

            # percepatan
            self.kecepatan +=  50
            #jarakTempuh -= kecepatan
            self.jarakTempuh += self.kecepatan

            labelJarakTempuh.config(text="jarak tempuh: "+str(self.jarakTempuh))
            labelKecepatan.config(text="kecepatan: "+str(self.kecepatan)+"Km/jam")

            root.after(500, lambda: self.masterControl(depan, belakang, depanKanan, depanKiri, kanan, kiri, traffic))

    def buildGui(self, depan, belakang, depanKanan, depanKiri, kanan, kiri, traffic):
        global root, labelJarakTempuh, labelKecepatan, labelJarakDepan, labelJarakBelakang, labelJarakKanan, labelJarakKiri, labelTraffic, labelDepanKanan, labelDepanKiri, labelTindakan
        root = Tk()
        gambar = PhotoImage("tes.jpg")
        labelJarakTempuh = Label(root)
        labelKecepatan = Label(root, image=gambar, fg="black", compound=CENTER)
        labelJarakDepan = Label(root)
        labelJarakBelakang = Label(root)
        labelJarakKanan = Label(root)
        labelJarakKiri = Label(root)
        labelTraffic = Label(root)
        labelDepanKanan = Label(root)
        labelDepanKiri = Label(root)
        labelTindakan = Label(root)
        #labelJarakTempuh.pack()
        labelKecepatan.pack()
        labelJarakDepan.pack()
        labelJarakBelakang.pack()
        labelJarakKanan.pack()
        labelJarakKiri.pack()
        labelTraffic.pack()
        labelDepanKanan.pack()
        labelDepanKiri.pack()
        labelTindakan.pack()
        self.masterControl(depan, belakang, depanKanan, depanKiri, kanan, kiri, traffic)
		
        root.mainloop()

    def main(self):

        DepanIN, DepanOUT = Pipe()
        BelakangIN, BelakangOUT = Pipe()
        KananIN, KananOUT = Pipe()
        KiriIN, KiriOUT = Pipe()
        DepanKananIN, DepanKananOUT = Pipe()
        DepanKiriIN, DepanKiriOUT = Pipe()
        TrafficIN, TrafficOUT = Pipe()
        ProsesKirimDepan = Process(target=self.kirimDepan, args=(DepanIN,))
        ProsesKirimDepanKiri = Process(target=self.kirimDepanKiri, args=(DepanKiriIN,))
        ProsesKirimDepanKanan = Process(target=self.kirimDepanKanan, args=(DepanKananIN,))
        ProsesKirimBelakang = Process(target=self.kirimBelakang, args=(BelakangIN,))
        ProsesKirimKanan = Process(target=self.kirimKanan, args=(KananIN,))
        ProsesKirimKiri = Process(target=self.kirimKiri, args=(KiriIN,))
        ProsesTraffic = Process(target=self.kirimTraffic, args=(TrafficIN,))
        BuildGui = Process(target=self.buildGui, args=(DepanOUT,BelakangOUT,DepanKananOUT,DepanKiriOUT,KananOUT,KiriOUT,TrafficOUT))

        ProsesKirimDepan.start()
        ProsesKirimDepanKiri.start()
        ProsesKirimDepanKanan.start()
        ProsesKirimBelakang.start()
        ProsesKirimKanan.start()
        ProsesKirimKiri.start()
        ProsesTraffic.start()
        BuildGui.start()

        ProsesKirimDepan.join()
        ProsesKirimDepanKiri.join()
        ProsesKirimDepanKanan.join()
        ProsesKirimBelakang.join()
        ProsesKirimKanan.join()
        ProsesKirimKiri.join()
        ProsesTraffic.join()
        BuildGui.join()

if __name__ == '__main__':
    utsv2().main()