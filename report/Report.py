from odoo import models
from odoo import http
from odoo.http import request

class PegawaiXlsx(models.AbstractModel):
    _name = 'report.pegawai.report_daftar_pegawai_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, pegawai):
        sheet = workbook.add_worksheet('Daftar Pegawai')
        bold = workbook.add_format({'bold': True})
        row, col = 0, 0
        fields = ['Id Pegawai','Nama Pegawai',  'Status', 'Role', 'Tanggal Lahir', 'Alamat', 'No KTP', 'No HP']
        for i in range(len(fields)):
            sheet.write(row, col, fields[i], bold)
            col += 1

        col = 0
        for obj in pegawai:
            row += 1
            sheet.write(row, col, obj.id)
            sheet.write(row, col+1, obj.name)
            sheet.write(row, col+2, obj.status)
            sheet.write(row, col+3, obj.role.name)
            sheet.write(row, col+4, obj.tgl_lahir)
            sheet.write(row, col+5, obj.alamat)
            sheet.write(row, col+6, obj.no_ktp)
            sheet.write(row, col+7, obj.no_hp)

class AbsenXlsx(models.AbstractModel):
    _name = 'report.pegawai.report_absensi_pegawai_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, absen):
        pegawai_daftar  = request.env['pegawai.pegawai'].search([])
        for pegawai in pegawai_daftar:
            sheet = workbook.add_worksheet(f'{pegawai.name[:31]}')
            bold = workbook.add_format({'bold': True})
            row, col = 0, 0
            sheet.write(row, col, "Tanggal", bold)
            sheet.write(row, col+1, "Jam Masuk", bold)
            sheet.write(row, col+2, "Jam Keluar", bold)
            sheet.write(row, col+3, "Durasi Kerja", bold)
            
            absen_pegawai = request.env['pegawai.absen'].search([('pegawai_id','=',pegawai.id)])
           
            for obj in absen_pegawai:
                print(obj.tanggal)
                row += 1
                sheet.write(row, col, obj.tanggal)
                sheet.write(row, col+1, obj.jam_masuk)
                sheet.write(row, col+2, obj.jam_keluar)
                sheet.write(row, col+3, obj.durasi_kerja)

class IzinXlsx(models.AbstractModel):
    _name = 'report.pegawai.report_izin_pegawai_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, absen):
        pegawai_daftar  = request.env['pegawai.pegawai'].search([])
        for pegawai in pegawai_daftar:
            sheet = workbook.add_worksheet(f'{pegawai.name[:31]}')
            bold = workbook.add_format({'bold': True})
            row, col = 0, 0
            sheet.write(row, col, "Tanggal Mulai", bold)
            sheet.write(row, col+1, "Tanggal Berakhir", bold)
            sheet.write(row, col+2, "Alasan", bold)
            sheet.write(row, col+3, "Jumlah Hari Izin", bold)
            
            absen_pegawai = request.env['pegawai.izin'].search([('pegawai_id','=',pegawai.id)])
           
            for obj in absen_pegawai:
                row += 1
                sheet.write(row, col, obj.tgl_izin_mulai)
                sheet.write(row, col+1, obj.tgl_izin_akhir)
                sheet.write(row, col+2, obj.alasan)
                sheet.write(row, col+3, obj.hari_izin)
            
            
            