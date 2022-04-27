from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException
from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, \
    CommentForm
from app.models import User, Post, Comment
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/mypost', methods=['GET', 'POST'])
@login_required
def mypost():
    page = request.args.get('page', 1, type=int)
    posts = current_user.posts.paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.mypost', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.mypost', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You are following %(username)s!', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You are not following %(username)s.', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})




@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.body = post.get_body()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.post.data, post_id=post_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash(_('Your comment is now live!'))
        return redirect(url_for('main.show_post',  post_id=post.id))


    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items





    return render_template('post.html', post=post, pagination=pagination, comments=comments, form=form)




@bp.route('/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        postuid = post.post_body(form.body.data)
        if not postuid:
            flash(_('Post fail!'))
            return redirect(url_for('main.index'))
        post.post_uid = postuid
        post.user_id = current_user.id
        post.title = form.title.data
        post.short_desc = form.body.data[:100]
        db.session.add(post)
        db.session.flush()
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.show_post',  post_id=post.id))

    return render_template('editpost.html',form=form)




@bp.route('/userid/<user_id>')
@login_required
def userid(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


