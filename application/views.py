from flask import current_app as app,render_template,request,redirect,url_for
from application.models import db,User,Songs,Playlist,RoleUsers
from application.sec import datastore
from flask_restful import marshal,fields
import os
#* This method is used for registration of users
@app.route("/",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        status = ''
        return render_template('index.html',status = status)
    elif request.method == 'POST':
        # print(request.form.get('u_name'),request.form.get('pass'))
        if not datastore.find_user(username = request.form.get('u_name')):
            try:
                datastore.create_user(username = request.form.get('u_name'), password = request.form.get('pass'), roles= ['user'])
            except:
                raise
            finally:
                db.session.commit()
                return redirect('/loginuser')
        else:
            status = 'User already exists'
            return render_template('index.html',status = status)

#* This method is used for the login of users
@app.route("/loginuser",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        status = ""
        return render_template('login.html',status = status)
    
    elif request.method == 'POST':
        user = datastore.find_user(username = request.form.get('u_name'))
        if not user:
            status = 'Invalid User'
            return render_template('login.html',status = status)
        if user.password == request.form.get('pass'):
            songs = Songs.query.all()
            return render_template('userhomepage.html' ,songs = songs)
        else:
            status = "Invalid Password"
            return render_template('login.html',status = status)
            

@app.route('/ratesongs',methods = ['GET','POST'])
def ratesongs():
    songs = Songs.query.all() 
    if request.method == 'GET':
        return render_template('userhomepage.html' ,songs = songs)

    if request.method == 'POST':
        song_id = request.form.get('song_id')
        rating= request.form.get('rating')
        try:
            song = Songs.query.get(song_id)
            song.rating += int(rating)
        except:
            raise
        finally:
            db.session.commit()
            return render_template('userhomepage.html',songs = songs)



@app.route('/adminlogin',methods = ['GET','POST'])
def adminlogin():
    if request.method == 'GET':
        status = ""
        return render_template('adminlogin.html',status = status)
    
    elif request.method == 'POST':
        user = datastore.find_user(username = request.form.get('u_name'))
        if user.password == request.form.get('pass'):
            return redirect('/home')
        else:
            status = "Invalid Password"
            return render_template('adminlogin.html',status = status)

@app.route('/creatorregister',methods=['GET','POST'])
def creator_register():
    if request.method == 'GET':
        return render_template('creatorregister.html')
    elif request.method == 'POST':
        if not datastore.find_user(username = request.form.get('u_name')):
            try:
                datastore.create_user(username = request.form.get('u_name'),password = request.form.get('pass'),roles = ['creator'])
            except:
                raise
            finally:
                return redirect('/creatorlogin')
        else:
            user  = datastore.find_user(username = request.form.get('u_name'))
            datastore.add_role_to_user(user=user,role='creator')
            db.session.commit()
            return "Creator role added"

@app.route('/creatorlogin',methods = ["GET","POST"])
def creatorlogin():
    if request.method == 'GET':
        return render_template('creatorlogin.html')
    elif request.method == 'POST':
        if datastore.find_user(username = request.form.get('u_name')):
            user = datastore.find_user(username = request.form.get('u_name'))
            if user.password == request.form.get('pass') and user.has_role('creator'):
                return redirect('/creatorhome')
            else:
                status = 'Invalid Credentials'
                return render_template('creatorlogin.html',status = status)
        else:
            status = 'User Not Found'
            return render_template('creatorlogin.html',status = status)
            

@app.route('/creatorhome',methods = ['GET','POST'])
def creatorhome():
    if request.method == 'GET':
        return render_template('creatorhomepage.html')
    elif request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and (file.filename.split('.')[-1] == 'mp3'):
            filename = os.path.join(app.config['SONG_UPLOAD_FOLDER'], file.filename)
            if os.path.exists(filename):
                return "File already exists"
            song = Songs(name=request.form.get('song_name'),artist = request.form.get('artist_name'), location = filename, lyrics = request.form.get('lyrics'))
            file.save(filename)
            try:
                db.session.add(song)
            except:
                raise
            finally:
                db.session.commit()
            return redirect(request.url)
        else:
            return "Invalid file type"
        

@app.route('/createplaylist',methods = ['GET','POST'])
def createplaylist():
    if request.method == 'GET':
        songs = Songs.query.all()
        return render_template('createplaylist.html', songs = songs)
    elif request.method == 'POST':
        playlist = Playlist(name = request.form.get('playlist_name'))
        db.session.add(playlist)
        db.session.commit()
        print("Working till here")
        # print(request.form.getlist('song_checkbox'))
        for song_id in request.form.getlist('songs_checkbox'):
            print("Working in the for loop")
            song = Songs.query.get(song_id)
            print(song)
            if song:
                playlist.songs.append(song)
        db.session.commit()
        return 'Playlist created'
        

@app.route('/viewplaylist',methods=['GET'])
def viewplaylist():
    if request.method == 'GET':
        playlists = Playlist.query.all() 
        playlist_songs = {playlist.name: [[song.name,song.location] for song in playlist.songs] for playlist in playlists}
        # print(playlist)
        return render_template('viewplaylist.html',playlists = playlists,playlist_songs = playlist_songs)

# todo: Look for changes in artisit name as well for this
@app.route('/editlyrics',methods=['GET','POST'])
def editlyrics():
    if request.method == "GET":
        songs = Songs.query.all()
        return render_template('editlyrics.html',songs = songs)

    elif request.method == 'POST':
        song_id = request.form.get('selected_song')
        edited_song = request.form.get('edited_lyrics')
        song = Songs.query.get(song_id)
        try:
            song.lyrics = edited_song
        except:
            raise
        finally:
            db.session.commit()
            status = "Lyrics edited successfully"
            return render_template('editlyrics.html',status = status)


@app.route('/deleteplaylist',methods=['GET','POST'])
def deleteplaylist():
    if request.method == 'GET':
        songs = Songs.query.all()
        return render_template('deleteplaylist.html',songs = songs)
    elif request.method == 'POST':
        selected_song = Songs.query.get(request.form.get('selected_song'))
        if not selected_song:
            return 'Song does not exists'

        try:
            os.remove(selected_song.location)
            db.session.delete(selected_song)
        except:
            raise
        finally:
            db.session.commit()
            status = 'Song deleted successfully'
            return render_template('deleteplaylist.html',status = status)

@app.route('/home',methods=['GET','POST'])
def homepage():
    if request.method == 'GET':
        users = RoleUsers.query.filter_by(role_id = '3').count()
        creators = RoleUsers.query.filter_by(role_id = '2').count()
        average_rating = db.session.query(db.func.avg(Songs.rating)).scalar()
        top_rated_songs = Songs.query.order_by(Songs.rating.desc()).limit(5)
        return render_template('adminhome.html',users = users,creators = creators,average_rating = average_rating,top_rated_songs = top_rated_songs)    
    

@app.route('/search',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        songs = Songs.query.filter(Songs.name.ilike(f'%{keyword}%') | Songs.artist.ilike(f'%{keyword}%')).all()
        return render_template('search.html', songs=songs)
    return render_template('search.html', songs=None)