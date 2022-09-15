from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Izin(models.Model):
    _name = 'pegawai.izin'
    _description = 'Pengajuan Izin'

    state = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('confirm', 'Confirm'),
                   ('approved', 'Approved'),
                   ('cancelled', 'Cancelled'),
                   ],
        required=True, readonly=True, default='draft')
    pegawai_id = fields.Many2one(comodel_name='pegawai.pegawai',string="Nama Pegawai", ondelete='cascade')
    tgl_izin_mulai = fields.Date(string='Tanggal Mulai Izin', readonly=(state != 'draft'))
    tgl_izin_akhir = fields.Date(string='Tanggal Berakhir Izin')
    alasan = fields.Text(string='Alasan Tidak Masuk')
    hari_izin = fields.Integer(string='Jumlah Hari Izin')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        record = super(Izin, self).create(vals)
        if record.tgl_izin_mulai and record.tgl_izin_akhir:
            record.hari_izin = (record.tgl_izin_akhir - record.tgl_izin_mulai).days + 1
            self.env['pegawai.pegawai'].search([('id','=',record.pegawai_id.id)]).write({'jatah_cuti':record.pegawai_id.jatah_cuti-record.hari_izin})
        return record
 
    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError("Tdak dapat menghapus jika status BUKAN DRAFT")
        else:
            self.env['pegawai.pegawai'].search([('id','=',self.pegawai_id.id)]).write({'jatah_cuti':self.pegawai_id.jatah_cuti+self.hari_izin})
        return super(Izin, self).unlink()

    @api.constrains('tgl_izin_mulai', 'tgl_izin_akhir')
    def check_tanggal(self):
        if self.tgl_izin_mulai > self.tgl_izin_akhir:
            raise ValidationError("Tanggal berakhir izin haruslah setelah tanggal mulai izin ")
