from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask import request

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dd793de789f6df5210f233ce4a83f92d'

postspy = [
   {
        'author': 'auteur 1',
        'title' : 'blog post 1',
        'content' : 'first post content',
        'date_posted' : 'April'        
   },
   {
        'author': 'auteur 2',
        'title' : 'blog post 2',
        'content' : 'qsddf post content',
        'date_posted' : 'may' 
    }
]


@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html',posts=postspy)

@app.route('/about')
def about():
  return render_template('about.html',title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
   form = RegistrationForm()
   if form.validate_on_submit():
      flash(f'Account created for {form.username.data}!', 'success')
      return redirect(url_for('home'))
   return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
      if form.email.data == 'simon.baecke@gmail.com' and form.password.data == "password":
         flash('you have been logged in!', 'success')
         return redirect(url_for('home'))
      else:
         flash('Login Unsuccesfull. Please check username and password', 'danger')
   return render_template('login.html', title='Login', form=form)

@app.route('/test')
def test():
   user_agent = request.headers.get('User-Agent')
   return user_agent




if __name__ == "__main__":
    app.run(debug=True) 