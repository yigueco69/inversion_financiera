# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import babel.messages.pofile
import base64
import csv
import datetime
import functools
import glob
import hashlib
import imghdr
import itertools
import jinja2
import json
import logging
import operator
import os
import re
import sys
import time
import werkzeug.utils
import werkzeug.wrappers
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO


import odoo
import odoo.modules.registry
from odoo.api import call_kw, Environment
from odoo.modules import get_resource_path
from odoo.tools import topological_sort
from odoo.tools.translate import _
from odoo.tools.misc import str2bool, xlwt
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
                      serialize_exception as _serialize_exception
from odoo.exceptions import AccessError, UserError
from odoo.models import check_method_name

_logger = logging.getLogger(__name__)

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.web', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps

# 1 week cache for asset bundles as advised by Google Page Speed
BUNDLE_MAXAGE = 60 * 60 * 24 * 7

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'

#----------------------------------------------------------
# Odoo Web helpers
#----------------------------------------------------------

db_list = http.db_list

db_monodb = http.db_monodb

class webservice(http.Controller):
    @http.route('/qwer', type='http', auth="none")
    def selector(self, **kw):
        # cp_merchant_id = '2c7b76970e7e4a26e9957f4b277c5ace'
        # cp_ipn_secret = 'porra69mejores132porra@69'
        # cp_debug_email = 'emanuelguerrero@hotmail.com'
        # import os
        # print os.path.dirname(__file__)
        # f = open(os.path.dirname(__file__)+'/holamundo.txt', 'w')
        # f.write(cp_merchant_id + cp_ipn_secret + cp_debug_email)
        # f.close()

        # def errorAndDie(error_msg):

        #     return 'IPN Error: ' + error_msg
        # return str(request.params)
        # # if _POST['ipn_mode'] is None or _POST['ipn_mode'] != 'hmac':
        # #     errorAndDie('IPN Mode is not HMAC.'. fputs($file, "IPN Mode is not HMAC")); 
        

        return "self._render_template(manage=False)"
