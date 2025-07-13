from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for, flash
from .services import (
    get_all_categories,
    get_categories_paginated,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
)

bp = Blueprint('categories', __name__, url_prefix='/categories')

# API routes
@bp.route('/api/', methods=['GET'])
def list_categories():
    categories = get_all_categories()
    return jsonify([category.__dict__ for category in categories])

@bp.route('/api/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = get_category_by_id(category_id)
    if not category:
        abort(404, description='Category not found')
    return jsonify(category.__dict__)

@bp.route('/api/', methods=['POST'])
def create():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    if not name:
        abort(400, description='Name is required')
    category = create_category(name, description)
    return jsonify(category.__dict__), 201

@bp.route('/api/<int:category_id>', methods=['PUT', 'PATCH'])
def update(category_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    category = update_category(category_id, name, description)
    if not category:
        abort(404, description='Category not found')
    return jsonify(category.__dict__)

@bp.route('/api/<int:category_id>', methods=['DELETE'])
def delete(category_id):
    success = delete_category(category_id)
    if not success:
        abort(404, description='Category not found')
    return '', 204

# UI routes
ui_prefix = '/'

@bp.route(f'{ui_prefix}', methods=['GET'])
def categories_list_ui():
    # Получаем параметры пагинации
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    # Валидируем per_page
    if per_page not in [6, 12, 24]:
        if per_page != -1:  # -1 означает "все"
            per_page = 12

    # Если per_page = -1, получаем все категории без пагинации
    if per_page == -1:
        categories = get_all_categories()
        total_count = len(categories)
        current_page = 1
        total_pages = 1
    else:
        categories, total_count, current_page, total_pages = get_categories_paginated(page, per_page)

    return render_template('categories/categories.html',
                        categories=categories,
                        current_page=current_page,
                        total_pages=total_pages,
                        total_count=total_count,
                        per_page=per_page)

@bp.route(f'{ui_prefix}new', methods=['GET', 'POST'])
def category_create_ui():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash('Name is required!', 'danger')
            return render_template('categories/category_form.html', category=None)
        create_category(name, description)
        flash('Category created!', 'success')
        return redirect(url_for('categories.categories_list_ui'))
    return render_template('categories/category_form.html', category=None)

@bp.route(f'{ui_prefix}<int:category_id>/edit', methods=['GET', 'POST'])
def category_edit_ui(category_id):
    category = get_category_by_id(category_id)
    if not category:
        abort(404, description='Category not found')
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash('Name is required!', 'danger')
            return render_template('categories/category_form.html', category=category)
        update_category(category_id, name, description)
        flash('Category updated!', 'success')
        return redirect(url_for('categories.categories_list_ui'))
    return render_template('categories/category_form.html', category=category)

@bp.route(f'{ui_prefix}<int:category_id>/delete', methods=['GET', 'POST'])
def category_delete_ui(category_id):
    category = get_category_by_id(category_id)
    if not category:
        abort(404, description='Category not found')
    if request.method == 'POST':
        delete_category(category_id)
        flash('Category deleted!', 'success')
        return redirect(url_for('categories.categories_list_ui'))
    return render_template('categories/category_delete.html', category=category)

@bp.route(f'{ui_prefix}<int:category_id>', methods=['GET'])
def category_detail_ui(category_id):
    category = get_category_by_id(category_id)
    if not category:
        abort(404, description='Category not found')
    return render_template('categories/category_detail.html', category=category)