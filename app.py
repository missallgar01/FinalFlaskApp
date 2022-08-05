from flask import Flask, render_template, request, url_for, redirect, session
from weather import Weather
from users import Users
from map import Map

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'

#Login interface
@app.route('/',methods=('GET', 'POST'))
def index():
    
    ##Initalise user class object
    user_login = Users()
    if request.method == 'POST':
        #store username as session variable
        session["username"] = request.form.get("username")
        password = request.form['password']
        
        print(session)
        print(session["username"])
        
        if user_login.authenticate(session["username"],password):
            return redirect(url_for('home'))
        else:
            #Remove session variable
            #session.pop('username', None)
            return redirect(url_for('index'))

    return render_template('index.html')

#Home page interface
@app.route('/home')
def home():
    #Authenticates session[username]
    print(session)
    #print(session["username"])
    if 'username' in session:
      return render_template('home.html')
    return redirect(url_for('index'))

#Dashboard interface
@app.route('/dashboard',methods=('GET', 'POST'))
def dashboard():
    #Initalise class objects
    data = Weather()
    my_map = Map()

    #Set default settings
    session["start"] = '00:00:00'
    session["end"] ='00:00:00'

    # Authenticates session[username]
    if 'username' in session:

        if request.method == 'POST':
            #Check clicked submit button
            if request.form['btn'] == 'Update':
                session["lat"] = request.form.get("lat")
                session["lon"] = request.form.get("lon")

            else:
                session["start"] = request.form.get("start")
                session["end"] = request.form.get("end")

            # Weather data

            response = data.getCurrentWeather(session["lat"], session["lon"])
            if response:
                data.save()
                humidity = data.getCurrentHumidity()
                temperature = data.getCurrentTemp()

                # Interactive weather map
                latlon = [(session["lat"], session["lon"] )]
                html_string = my_map.scatterplot_map(latlon)
                # html_string = my_map.choropleth()

                #Filter data and display in table
                filter = data.filterWeatherData(session["start"], session["end"])

                # weather graph
                legend = 'Monthly Data'
                labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
                values = [10, 9, 8, 7, 6, 4, 7, 8]

                return render_template('dashboard.html', humidity=humidity, temp=temperature, values=values,
                                       labels=labels, legend=legend, div_placeholder=html_string,
                                       filter=[filter.to_html()], titles=[''])
            else:
                return render_template('dashboard.html',msg="Invalid")

        return render_template('dashboard.html')
    return redirect(url_for('index'))

#The application also contains a logout () view function that pops up the 'username' session variable.Therefore, the ' /' URL displays the start page again.
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
