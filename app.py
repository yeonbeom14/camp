from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.wpcmaxy.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/profils", methods=["POST"])
def profils_post():
    name_receive = request.form['name_give']
    age_receive = request.form['age_give']
    area_receive = request.form['area_give']
    mbti_receive = request.form['mbti_give']
    hobby_receive = request.form['hobby_give']
    picurl_receive = request.form['picurl_give']
    description_receive = request.form['description_give']

    doc = {
        'name':name_receive,
        'age':age_receive,
        'area':area_receive,
        'mbti':mbti_receive,
        'hobby':hobby_receive,
        'picurl':picurl_receive,
        'description':description_receive,
    }
    db.profils.insert_one(doc)

    return jsonify({'msg': '프로필 저장 완료!'})

@app.route("/profils", methods=["GET"])
def profils_get():
    all_profils = list(db.profils.find({}))
    for row in all_profils:
        row["_id"] = str(row["_id"])
    return jsonify({'result': all_profils})

@app.route("/profils/<id>", methods=["GET"])
def profil_get(id):

    profil = db.profils.find_one({'_id':ObjectId(str(id))})
    profil["_id"] = str(profil["_id"])
    return jsonify({'profil': profil})

@app.route("/profils/<id>", methods=["DELETE"])
def profil_remove(id):

    db.profils.delete_one({'_id':ObjectId(str(id))})

    return jsonify({'msg': '삭제 완료!'})

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    user_receive = request.form['user_give']
    comment_receive = request.form['comment_give']
    doc = {
        'user':user_receive,
        'comment':comment_receive
    }
    db.cmt.insert_one(doc)

    return jsonify({'msg': '방명록 저장 완료!'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.cmt.find({}))
    for row in all_comments:
        row["_id"] = str(row["_id"])
    return jsonify({'result': all_comments})

@app.route("/guestbook/<id>", methods=["DELETE"])
def comment_remove(id):

    db.cmt.delete_one({'_id':ObjectId(str(id))})

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)