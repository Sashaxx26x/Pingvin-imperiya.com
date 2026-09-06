import os
import sys

# Автоматическая установка зависимостей
try:
    from flask import Flask, render_template_string, request, session, redirect
    from datetime import datetime
    import hashlib
except ImportError:
    os.system(f'{sys.executable} -m pip install flask')
    os.system(f'{sys.executable} -m pip install gunicorn')
    from flask import Flask, render_template_string, request, session, redirect
    from datetime import datetime
    import hashlib

app = Flask(__name__)
app.secret_key = 'секретный_ключ'

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐧 Пингвин Империя</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 15px;
        }
        .контейнер { max-width: 800px; margin: 0 auto; }
        .шапка {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .карточка {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .кнопка {
            display: inline-block;
            padding: 12px 25px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1em;
        }
        .кнопка:hover { background: #5a67d8; }
        .кнопка-зеленая { background: #48bb78; }
        .кнопка-желтая { background: #ed8936; }
        .кнопка-красная { background: #f56565; }
        input {
            padding: 12px;
            margin: 8px 0;
            border-radius: 10px;
            border: 1px solid #ddd;
            width: 100%;
            font-size: 1em;
        }
        .баланс {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 15px;
        }
        .баланс-пункт {
            background: #f7fafc;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            flex: 1;
            min-width: 150px;
        }
        .пингвин {
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        .навигация {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 15px 0;
        }
        h1, h2, h3 { margin-bottom: 15px; }
        .вип { color: #d69e2e; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
    </style>
</head>
<body>
    <div class="контейнер">
        <div class="шапка">
            <h1>🐧 Пингвин Империя</h1>
            {% if пользователь %}
            <p>Привет, <strong>{{ пользователь['почта'] }}</strong>! 
                {% if пользователь['вип'] %}<span class="вип">👑 VIP</span>{% endif %}
                {% if пользователь['админ'] %}<span style="color: #e53e3e;">👑 Админ</span>{% endif %}
            </p>
            {% endif %}
        </div>
        
        {% if пользователь %}
            <div class="баланс карточка">
                <div class="баланс-пункт">
                    <h3>💰 Баланс</h3>
                    <p style="font-size: 1.5em;">{{ "%.2f"|format(пользователь['баланс']) }} ₽</p>
                </div>
                <div class="баланс-пункт">
                    <h3>🐟 Рыба</h3>
                    <p style="font-size: 1.5em;">{{ "%.2f"|format(пользователь['рыба']) }} кг</p>
                </div>
                <div class="баланс-пункт">
                    <h3>📈 Доход/час</h3>
                    <p style="font-size: 1.5em;">{{ "%.2f"|format(доход) }} ₽</p>
                </div>
            </div>
            
            <div class="навигация">
                <a href="/магазин" class="кнопка">🛒 Магазин</a>
                <a href="/продать_рыбу" class="кнопка кнопка-зеленая">💰 Продать рыбу</a>
                <a href="/бонус" class="кнопка кнопка-желтая">🎁 Бонус</a>
                {% if пользователь['админ'] %}
                <a href="/админ" class="кнопка кнопка-красная">👑 Админ</a>
                {% endif %}
                <a href="/выход" class="кнопка кнопка-красная">🚪 Выйти</a>
            </div>
            
            {% if страница == 'магазин' %}
                <h2>🛒 Магазин пингвинов</h2>
                {% for п in список_пингвинов %}
                <div class="пингвин карточка">
                    <h3>{{ п['название'] }} {{ п['эмодзи'] }}</h3>
                    <p>💰 Цена: {{ п['цена'] }} ₽</p>
                    <p>📈 Доход: {{ п['доход'] }} ₽/час</p>
                    <p>⏱ Окупаемость: {{ "%.1f"|format(п['цена'] / п['доход']) }} часов</p>
                    <a href="/купить/{{ п['ид'] }}" class="кнопка">Купить</a>
                </div>
                {% endfor %}
                
            {% elif страница == 'админ' and пользователь['админ'] %}
                <h2>👑 Админ-панель</h2>
                <div class="карточка">
                    <h3>Пользователи</h3>
                    <table>
                        <tr>
                            <th>Почта</th>
                            <th>Баланс</th>
                            <th>Рыба</th>
                            <th>VIP</th>
                            <th>Действия</th>
                        </tr>
                        {% for польз in все_пользователи %}
                        <tr>
                            <td>{{ польз['почта'] }}</td>
                            <td>{{ "%.2f"|format(польз['баланс']) }} ₽</td>
                            <td>{{ "%.2f"|format(польз['рыба']) }} кг</td>
                            <td>{{ '✅' if польз['вип'] else '❌' }}</td>
                            <td>
                                <form method="POST" action="/админ/пополнить/{{ польз['почта'] }}" style="display: inline;">
                                    <input type="number" name="сумма" placeholder="Сумма" step="0.01" style="width: 100px; display: inline;">
                                    <button type="submit" class="кнопка">💰</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                
            {% else %}
                <h2>Ваши пингвины:</h2>
                {% if пользователь['пингвины'] %}
                    {% for п in пользователь['пингвины'] %}
                    <div class="пингвин карточка">
                        <h3>{{ п['название'] }} {{ п['эмодзи'] }}</h3>
                        <p>Количество: {{ п['количество'] }}</p>
                        <p>Доход: {{ "%.2f"|format(п['доход'] * п['количество'] * (2 if пользователь['вип'] else 1)) }} ₽/час</p>
                    </div>
                    {% endfor %}
                {% else %}
                    <p>У вас пока нет пингвинов. <a href="/магазин">Купить первого!</a></p>
                {% endif %}
            {% endif %}
            
        {% else %}
            <div class="карточка">
                <h2>Вход</h2>
                <form method="POST" action="/вход">
                    <input type="email" name="почта" placeholder="Ваша почта" required>
                    <input type="password" name="пароль" placeholder="Пароль" required>
                    <button type="submit" class="кнопка">Войти</button>
                </form>
                <p style="margin-top: 15px;">Нет аккаунта?</p>
                <a href="/регистрация" class="кнопка">Регистрация</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

# Данные
пользователи = {}
список_пингвинов = [
    {'ид': 1, 'название': 'Птенец', 'цена': 50, 'доход': 1.5, 'эмодзи': '🐣'},
    {'ид': 2, 'название': 'Джентельмен', 'цена': 250, 'доход': 7, 'эмодзи': '🎩'},
    {'ид': 3, 'название': 'Шахтёр', 'цена': 1000, 'доход': 30, 'эмодзи': '⛏'},
    {'ид': 4, 'название': 'Ледяной маг', 'цена': 5000, 'доход': 160, 'эмодзи': '🧊'},
    {'ид': 5, 'название': 'Император', 'цена': 25000, 'доход': 850, 'эмодзи': '👑'},
    {'ид': 6, 'название': 'Космопингвин', 'цена': 100000, 'доход': 3500, 'эмодзи': '🚀'},
]

def хеш_пароля(пароль):
    return hashlib.sha256(пароль.encode()).hexdigest()

def посчитать_доход(пользователь):
    доход = 0
    for п in пользователь['пингвины']:
        доход += п['доход'] * п['количество']
    if пользователь['вип']:
        доход *= 2
    return доход

@app.route('/')
def главная():
    if 'пользователь' not in session:
        return render_template_string(HTML, пользователь=None)
    
    пользователь = пользователи.get(session['пользователь'])
    if not пользователь:
        session.pop('пользователь', None)
        return redirect('/')
    
    return render_template_string(HTML, 
                                пользователь=пользователь,
                                доход=посчитать_доход(пользователь),
                                страница='главная')

@app.route('/регистрация', methods=['GET', 'POST'])
def регистрация():
    if request.method == 'POST':
        почта = request.form['почта'].strip().lower()
        пароль = request.form['пароль']
        
        if '@' not in почта or '.' not in почта:
            return 'Введите корректную почту!'
        
        if len(пароль) < 6:
            return 'Пароль слишком короткий! Минимум 6 символов.'
        
        if почта in пользователи:
            return 'Пользователь с такой почтой уже существует!'
        
        пользователи[почта] = {
            'почта': почта,
            'пароль': хеш_пароля(пароль),
            'баланс': 10.0,
            'рыба': 0.0,
            'пингвины': [],
            'вип': False,
            'админ': False,
            'бонус_дата': None
        }
        session['пользователь'] = почта
        return redirect('/')
    
    return render_template_string(HTML, пользователь=None)

@app.route('/вход', methods=['POST'])
def вход():
    почта = request.form['почта'].strip().lower()
    пароль = хеш_пароля(request.form['пароль'])
    
    if почта in пользователи and пользователи[почта]['пароль'] == пароль:
        session['пользователь'] = почта
        return redirect('/')
    
    return 'Неверная почта или пароль!'

@app.route('/выход')
def выход():
    session.pop('пользователь', None)
    return redirect('/')

@app.route('/магазин')
def магазин():
    if 'пользователь' not in session:
        return redirect('/')
    
    пользователь = пользователи[session['пользователь']]
    return render_template_string(HTML,
                                пользователь=пользователь,
                                страница='магазин',
                                список_пингвинов=список_пингвинов,
                                доход=посчитать_доход(пользователь))

@app.route('/купить/<int:ид>')
def купить(ид):
    if 'пользователь' not in session:
        return redirect('/')
    
    пользователь = пользователи[session['пользователь']]
    пингвин = next((п for п in список_пингвинов if п['ид'] == ид), None)
    
    if not пингвин:
        return 'Пингвин не найден!'
    
    if пользователь['баланс'] < пингвин['цена']:
        return 'Недостаточно средств!'
    
    пользователь['баланс'] -= пингвин['цена']
    
    существующий = next((п for п in пользователь['пингвины'] if п['ид'] == ид), None)
    if существующий:
        существующий['количество'] += 1
    else:
        пользователь['пингвины'].append({
            'ид': пингвин['ид'],
            'название': пингвин['название'],
            'доход': пингвин['доход'],
            'эмодзи': пингвин['эмодзи'],
            'количество': 1
        })
    
    return redirect('/магазин')

@app.route('/продать_рыбу')
def продать_рыбу():
    if 'пользователь' not in session:
        return redirect('/')
    
    пользователь = пользователи[session['пользователь']]
    количество = пользователь['рыба']
    пользователь['баланс'] += количество
    пользователь['рыба'] = 0
    
    return redirect('/')

@app.route('/бонус')
def бонус():
    if 'пользователь' not in session:
        return redirect('/')
    
    пользователь = пользователи[session['пользователь']]
    сегодня = datetime.now().date()
    
    if пользователь['бонус_дата'] == сегодня:
        return 'Бонус уже получен сегодня!'
    
    сумма = 50 if пользователь['вип'] else 5
    пользователь['баланс'] += сумма
    пользователь['бонус_дата'] = сегодня
    
    return redirect('/')

@app.route('/админ')
def админ():
    if 'пользователь' not in session:
        return redirect('/')
    
    пользователь = пользователи[session['пользователь']]
    if not пользователь['админ']:
        return 'Доступ запрещён!'
    
    return render_template_string(HTML,
                                пользователь=пользователь,
                                страница='админ',
                                все_пользователи=list(пользователи.values()),
                                доход=посчитать_доход(пользователь))

@app.route('/админ/пополнить/<почта>', methods=['POST'])
def админ_пополнить(почта):
    if 'пользователь' not in session:
        return redirect('/')
    
    админ = пользователи[session['пользователь']]
    if not админ['админ']:
        return 'Доступ запрещён!'
    
    сумма = float(request.form['сумма'])
    if почта in пользователи:
        пользователи[почта]['баланс'] += сумма
    
    return redirect('/админ')

# Создание админа
def создать_админа():
    if 'админ@пингвин.рф' not in пользователи:
        пользователи['админ@пингвин.рф'] = {
            'почта': 'админ@пингвин.рф',
            'пароль': хеш_пароля('админ123'),
            'баланс': 10000000.0,
            'рыба': 0.0,
            'пингвины': [],
            'вип': True,
            'админ': True,
            'бонус_дата': None
        }
        for п in список_пингвинов:
            пользователи['админ@пингвин.рф']['пингвины'].append({
                'ид': п['ид'],
                'название': п['название'],
                'доход': п['доход'],
                'эмодзи': п['эмодзи'],
                'количество': 10
            })

# Создаём админа при запуске
создать_админа()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
