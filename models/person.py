from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Person(models.Model):
    _name = 'pegawai.person'
    _description = 'desc'
    
    name = fields.Char(string="Nama Pegawai")
    no_ktp = fields.Char(string="Nomor KTP")
    status = fields.Selection([
        ("Internship","Internship"),
        ("Part Time","Part Time"),
        ("Full Time","Full Time"),
    ],
        string="Tipe Pegawai",
        default = "Full Time"
    )
    alamat = fields.Char(string="Alamat")
    no_hp = fields.Char(string="Nomor HP")
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    role = fields.Many2one(comodel_name='pegawai.role', string="Role Pekerjaan", ondelete='cascade')
    
    @api.constrains('no_hp', 'no_ktp')
    def check_numeric(self):
        for rec in self:
            if type(rec.no_hp) != bool:
                if  not rec.no_hp.isdigit():
                    raise ValidationError("No HP tidak valid (harus berupa angka)")

            if type(rec.no_ktp) != bool:
                if  not rec.no_ktp.isdigit():
                    raise ValidationError("No KTP tidak valid (harus berupa angka)")
            

class Pegawai(models.Model):
    _name = 'pegawai.pegawai'
    _inherit = 'pegawai.person'
    _description = 'Pegawai Perusahaan'

    foto = fields.Image(string="Foto")
    jatah_cuti = fields.Integer(string="Jatah Cuti (hari)", default=10)
    absensi_ids = fields.One2many(comodel_name='pegawai.absen', inverse_name="pegawai_id", string="Absensi")
    izin_ids = fields.One2many(comodel_name='pegawai.izin', inverse_name="pegawai_id", string="Izin Pegawai")
    
    @api.constrains('jatah_cuti')
    def check_tanggal(self):
        print(self.jatah_cuti)
        if self.jatah_cuti < 0:
            raise ValidationError("Jatah Cuti Tidak Mencukupi")

class Pelamar(models.Model):
    _name = 'pegawai.pelamar'
    _inherit = 'pegawai.person'
    _description = 'Calon Pegawai Perusahaan'

    cv = fields.Binary(string='CV', attachment=True, required=True)
    cv_name = fields.Char(String='File Name1')
    
    @api.constrains('cv')
    def _check_file(self):
       if str(self.cv_name.split(".")[1]) != 'pdf' :
            raise ValidationError("File yang diupload haruslah pdf")

    def action_terima(self):
        self.env['pegawai.pegawai'].create({
            'name':self.name,
            'no_ktp':self.no_ktp,
            'status':self.status,
            'alamat':self.alamat,
            'no_hp':self.no_hp,
            'tgl_lahir':self.tgl_lahir,
            'role':self.role.id,
        })
        super(Pelamar,self).unlink()
    