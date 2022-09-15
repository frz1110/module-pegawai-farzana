

from odoo import http, models
from odoo.http import request
import json

class Pegawai(http.Controller):
     @http.route('/pegawai/get_pegawai', auth='public', method=['GET'])
     def get_barang(self, **kw):
         pegawai_data = request.env['pegawai.pegawai'].search([])
         isi = []
         for obj in pegawai_data:
            isi.append({
                'Nama Pegawai':obj.name, 
                'Id Pegawai': obj.id_pegawai, 
                'Status':obj.status,
                'Role':obj.role.name,
                'Tanggal Lahir':str(obj.tgl_lahir),
                'Alamat':obj.alamat, 
                'No KTP':obj.no_ktp, 
                'No HP':obj.no_hp,
            })
         return json.dumps(isi)
