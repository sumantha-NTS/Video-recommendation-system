from flask import Flask, request, render_template
import pickle 
import pandas as pd

app = Flask(__name__)

cos_model = pickle.load(open('df.csv','rb'))
dataset = pickle.load(open('dataset.csv','rb'))

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/results',methods=['POST'])
def results():
    search = request.form['search']
    x = [];z=pd.DataFrame(columns=dataset.columns)
    for i in range(0, len(dataset)):
        if dataset.Title[i].lower().find(search.lower()) >= 0:
            x.append(dataset.iloc[i, :])
    try:
        sel_df = pd.DataFrame(x).sort_values('rating', ascending=False)
        res = cos_model.iloc[:, sel_df.index[0]].sort_values(ascending=False).head(10).index
        for i in res:
            z = z.append(dataset[dataset.Title == i])
        z.reset_index(drop=True)
        res = z
        type1 = 'found'

    except:
        type1 = 'Not Found'
        res = None
    return render_template('results.html',x=[type1,res])

if __name__ == "__main__":
    app.run(debug=True)