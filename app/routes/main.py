from flask import Flask, Blueprint, render_template, request, redirect, url_for
from supabase import create_client, Client
from app import supabase
from dotenv import load_dotenv

main_bp = Blueprint('main', __name__) 

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_nama = request.form.get('input_nama')
        input_email = request.form.get('input_email')

        if input_nama and input_email:
            supabase.table('user_data')\
            .insert({
                "nama": input_nama,
                "email": input_email
            }).execute()
        return redirect(url_for('main.index'))

    respons = supabase.table('user_data').select('*').order('id', desc=False).execute()
    return render_template('main.html', data_pengguna=respons.data, pengguna_edit=None)

@main_bp.route('/edit/<int:id>', methods=['GET'])
def edit_form(id):
    respons_all = supabase.table('user_data').select('*').order('id', desc=False).execute()
    respons_single = supabase.table('user_data').select('*').order('id', id).execute()

    if not respons_single.data:
        return "Data tidak ditemukan", 404

    return render_template('main.html', data_pengguna=respons_all.data, pengguna_edit=respons_single.data[0])

@main_bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    update_nama = request.get.form('input_nama')
    update_email = request.get.form('input_email')

    supabase.table('user_data')\
    .update({
        "nama": update_nama,
        "email": update_email
    }).eq("id", id).execute()
    return redirect(url_for('main.index'))

@main_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    supabase.table('user_data').delete().eq("id", id).execute()
    return redirect(url_for('main.index'))