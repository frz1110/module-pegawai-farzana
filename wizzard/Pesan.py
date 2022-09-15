from odoo import models, fields, api


class Pesan(models.TransientModel):
     _name = 'pegawai.pesan'

     pesan = fields.Text(string='Pesan untuk HR')

     def button_kirim_pesan(self):
        pass

    
class PesanPegawai(models.TransientModel):
     _name = 'pegawai.pesan_pegawai'
     _inherit='pegawai.pesan'

     pegawai_id = fields.Many2one(comodel_name='pegawai.pegawai', string='Nama Pegawai')

     
class PesanPelamar(models.TransientModel):
     _name = 'pegawai.pesan_pelamar'
     _inherit='pegawai.pesan'

     pelamar_id = fields.Many2one(comodel_name='pegawai.pelamar', string='Nama Pelamar')
     pesan = fields.Text(string='Pesan untuk HR')
