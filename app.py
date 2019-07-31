# 此页面导入sweeppig下的 SweetPig与render_template
# 用法如下
from sweetpig import SweetPig, render_template
app = SweetPig(__name__)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/kami')
def home():
    return 'hello kami'

# 只要是在/blog/下的英文数字都会转到regular.html页面
@app.route('/blog/<id>')
def query_note(id):
    return render_template('Regular.html')
