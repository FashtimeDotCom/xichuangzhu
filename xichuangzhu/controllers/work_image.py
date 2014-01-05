# coding: utf-8
from __future__ import division
import os
import uuid
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app, db, config
from ..models import Work, WorkImage, CollectWorkImage
from ..forms import WorkImageForm
from ..utils import require_login


@app.route('/work_image/<int:work_image_id>', methods=['GET'])
def work_image(work_image_id):
    """作品的单个相关图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    if 'user_id' in session:
        is_collected = CollectWorkImage.query.filter(CollectWorkImage.user_id == session['user_id']).filter(
            CollectWorkImage.work_image_id == work_image_id).count() > 0
    else:
        is_collected = False
    return render_template('work_image/work_image.html', work_image=work_image, is_collected=is_collected)


@app.route('/work_image/<int:work_image_id>/delete', methods=['GET'])
@require_login
def delete_work_image(work_image_id):
    """删除作品的相关图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    if work_image.user_id != session['user_id']:
        abort(404)
    # delete image file
    if os.path.isfile(config.IMAGE_PATH + work_image.filename):
        os.remove(config.IMAGE_PATH + work_image.filename)
    db.session.delete(work_image)
    db.session.commit()
    return redirect(url_for('work', work_id=work_image.work_id))


@app.route('/work_image/<int:work_image_id>/collect', methods=['GET'])
@require_login
def collect_work_image(work_image_id):
    """收藏作品图片"""
    collect = CollectWorkImage(user_id=session['user_id'], work_image_id=work_image_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('work_image', work_image_id=work_image_id))


@app.route('/work_image/<int:work_image_id>/discollect', methods=['GET'])
@require_login
def discollect_work_image(work_image_id):
    """取消收藏作品图片"""
    db.session.query(CollectWorkImage).filter(CollectWorkImage.user_id == session['user_id']).filter(
        CollectWorkImage.work_image_id == work_image_id).delete()
    db.session.commit()
    return redirect(url_for('work_image', work_image_id=work_image_id))


@app.route('/all_work_images', methods=['GET'])
def all_work_images():
    """作品的所有相关图片"""
    page = int(request.args.get('page', 1))
    paginator = WorkImage.query.paginate(page, 12)
    return render_template('work_image/work_images.html', paginator=paginator)


@app.route('/work/<int:work_id>/add_image', methods=['GET', 'POST'])
@require_login
def add_work_image(work_id):
    """为作品添加相关图片"""
    work = Work.query.get_or_404(work_id)
    form = WorkImageForm()
    if form.validate_on_submit():
        # Save image
        image = request.files['image']
        image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
        image.save(config.IMAGE_PATH + image_filename)

        work_image = WorkImage(work_id=work_id, user_id=session['user_id'], url=config.IMAGE_URL + image_filename,
                               filename=image_filename)
        db.session.add(work_image)
        db.session.commit()
        return redirect(url_for('work_image', work_image_id=work_image.id))
    return render_template('work_image/add_work_image.html', work=work, form=form)


@app.route('/work_image/<int:work_image_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_work_image(work_image_id):
    """编辑作品的相关图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    form = WorkImageForm()
    if form.validate_on_submit():
        # Delete old image
        if os.path.isfile(config.IMAGE_PATH + work_image.filename):
            os.remove(config.IMAGE_PATH + work_image.filename)

        # Save new image
        image = request.files['image']
        image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
        image.save(config.IMAGE_PATH + image_filename)

        # update image info
        work_image.url = config.IMAGE_URL + image_filename
        work_image.filename = image_filename
        db.session.add(work_image)
        db.session.commit()
        return redirect(url_for('work_image', work_image_id=work_image_id))
    return render_template('work_image/edit_work_image.html', work_image=work_image, form=form)