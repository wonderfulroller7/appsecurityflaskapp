import os
import subprocess
from flask import Blueprint, render_template, redirect, g, url_for, request, session

import database
from login import isLoggedIn

root_view = Blueprint('spellchecker', __name__)

@root_view.route('/spell_check', methods=['GET', 'POST'])
@isLoggedIn
def spell_check():
    if request.method == 'POST':
        
        # print(request.headers.get['origin'])

        string_to_be_checked = request.form['inputtext']

        input_file = str(session.get('session-id')) + '.txt'
        print(string_to_be_checked)
        f = open(input_file, 'w')
        f.write(string_to_be_checked)
        f.close()
        arguments = ("./spell_check", str(input_file), "dictionary.txt")
        try:
            shell_process = subprocess.Popen(arguments, stdout=subprocess.PIPE)
            shell_process.wait()
            shell_output = shell_process.stdout.read()
            shell_output = shell_output.decode().replace("\n",",")
            print("Misspelled words : ", shell_output)
        except subprocess.CalledProcessError as e:
            print('Error :', e)

        return render_template('/spellreview.html', string_query=string_to_be_checked, misspelled=shell_output)
    else:
        return render_template('/spellchecker.html')

@root_view.after_request
def cache(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response