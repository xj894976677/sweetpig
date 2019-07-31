# 此页面导入sweeppig下的 SweetPig与render_template
# 用法如下
from sweetpig import SweetPig
from sweetpig import render_template
app = SweetPig(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/kami')
def home():
    return 'hello kami'
