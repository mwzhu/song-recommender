from flask import Flask, render_template, request
from main import recommend, unique_songs, print_songs

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        songs = list()
        for i in range(1,4):
            if request.form["song"+str(i)] is not None:
                songs.append(request.form["song"+str(i)])
        result = recommend(songs)
        return render_template('recommend.html',  tables=[result.to_html(classes='data', header="true", index=False, justify='center')])

    song_list = print_songs()
    return render_template('home.html', song_list=song_list)

@app.route("/songlist")
def songlist():
    result = unique_songs()
    return render_template('songlist.html',  tables=[result.to_html(classes='data', header="true", justify='center')])

if __name__ == '__main__':
    app.run()
