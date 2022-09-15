from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Absensi(models.Model):
    _name = 'pegawai.absen'
    _description = 'Absensi Perusahaan'

    pegawai_id = fields.Many2one(comodel_name='pegawai.pegawai',string="Nama Pegawai", ondelete='cascade')
    tanggal = fields.Date(string='Tanggal',readonly=True, default=fields.Datetime.now())
    jam_masuk = fields.Float(string='Jam Masuk')
    jam_keluar = fields.Float(string='Jam Keluar')
    durasi_kerja = fields.Float(string='Durasi Kerja')

    @api.onchange('jam_masuk', 'jam_keluar')
    def _compute_durasi_kerja(self):
        if self.jam_keluar and self.jam_masuk:
            self.durasi_kerja = self.jam_keluar  - self.jam_masuk

    @api.constrains('jam_masuk', 'jam_keluar')
    def check_tanggal(self):
        if self.jam_masuk > self.jam_keluar:
            raise ValidationError("Jam Pulang haruslah setelah Jam Mulai ")







