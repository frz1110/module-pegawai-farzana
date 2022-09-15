from odoo import models, fields, api


class Role(models.Model):
    _name = 'pegawai.role'
    _description = 'Absensi Perusahaan'

    pegawai_id = fields.One2many(comodel_name='pegawai.pegawai', inverse_name="role", string="Nama Pegawai")
    name = fields.Char(string='Role Pekerjaan')
    job_desc = fields.Text(string='Job Description')
    req = fields.Text(string='Requirements')
    pegawai_total = fields.Integer(compute='_compute_pegawai', string='Jumlah Pegawai Total')
    pegawai_intern = fields.Integer(compute='_compute_pegawai', string='Jumlah Pegawai Internship')
    pegawai_part = fields.Integer(compute='_compute_pegawai', string='Jumlah Pegawai Part Time')
    pegawai_full = fields.Integer(compute='_compute_pegawai', string='Jumlah Pegawai Full Time')

    _sql_constraints = [
        ('role_pekerjaan_unik', 'unique (name)', 'Nama Pekerjaan tidak boleh sama !!!')
    ]

    @api.depends('pegawai_intern')
    def _compute_pegawai(self):
        for record in self:
            record.pegawai_intern = self.env['pegawai.pegawai'].search_count([('status','=','Internship'),('role','=',record.name)])
            record.pegawai_part = self.env['pegawai.pegawai'].search_count([('status','=','Part Time'),('role','=',record.name)])
            record.pegawai_full = self.env['pegawai.pegawai'].search_count([('status','=','Full Time'),('role','=',record.name)])
            record.pegawai_total = record.pegawai_intern + record.pegawai_part + record.pegawai_full

