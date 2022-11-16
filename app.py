import datetime
from flask import Flask, render_template, request, session, redirect, url_for, make_response

app = Flask(__name__)
from db_util import Database

db = Database()
app.secret_key = "111"
app.permanent_session_lifetime = datetime.timedelta(days=365)


@app.route('/', methods=['get'])
def main():
    if 'user' in session:
        id = session['user']
        name = db.select(f"select first_name from users where id = '{id}'")
        return render_template("main.html", name=name)
    else:
        return render_template("main.html")


@app.route('/', methods=['post'])
def main_post():
    search = request.form.get('search')
    print(search)
    items = db.select(f"select item_name, cat_id name from items")
    print(items)
    for i in items:
        if i['item_name'] == search:
            c = i['name']
            print("fount")
            return redirect(url_for("category", cat_id=c))
    print(items)
    return render_template('main_no_match.html')


@app.route('/like/<int:item_id>')
def like(item_id):
    print('liked')
    if 'user' in session:
        id = session['user']
        cat_id = db.select(f"select cat_id from items where id={item_id}")
        print(cat_id['cat_id'])
        like_id = db.select(f"select id from likes where user_id = '{id}' and item_id = '{item_id}'")
        if like_id:
            db.insert(f"delete from likes where user_id = '{id}' and item_id = '{item_id}'")
        else:
            db.insert(f"insert into likes (user_id, item_id, liked) values ('{id}', '{item_id}', 'true')")
        return redirect(url_for('category', cat_id=cat_id['cat_id']))
    else:
        #  add new html with message that people must be authorized
        return redirect(url_for('auth_get'))

@app.route('/takeorder')
def take_order():
    id = session['user']
    basks = db.select(f"select item_id from basket where user_id = '{id}'")
    print(basks)
    bask_list = []
    if len(basks) >= 2:
        for i in basks:
            bask_list.append(i['item_id'])
    elif len(basks) == 1:
        bask_list.append(basks['item_id'])
    for i in bask_list:
        db.insert(f"insert into orders (user_id, item_id) values ('{id}', '{i}')")
        db.insert(f"delete from basket where user_id = '{id}' and item_id = '{i}'")
    return redirect(url_for('orders'))



@app.route("/orders")
def orders():
    id = session['user']
    ids = db.select(f"select item_id from orders where user_id = '{id}'")
    ids_list = set()
    if len(ids) >= 2:
        for i in ids:
            ids_list.add(i['item_id'])
    elif len(ids) == 1:
        ids_list.add(ids['item_id'])
    ids_l = tuple(ids_list)
    items = []
    if len(ids_l) > 1:
        items = db.select(f"select * from items where id in {ids_l}")
    elif len(ids_l) == 1:
        print('aaaaaaaa')
        print(ids_l)
        print(ids_l[0])
        items = db.select(f"select * from items where id = {ids_l[0]}")
        items = [items]
    basks = db.select(f"select item_id from basket where user_id = '{id}'")

    bask_list = []
    if len(basks) >= 2:
        for i in basks:
            bask_list.append(i['item_id'])
    elif len(basks) == 1:
        bask_list.append(basks['item_id'])
    print('bask list')
    print(bask_list)
    print(basks)
    context = {
        'title': {"cat_name": 'Orders'},
        'items': items,
        'desc': 'your liked list',
        'ids': ids_list,
        'bask': bask_list
    }
    return render_template('orders.html', **context)


@app.route('/likelike/<int:item_id>')
def like_like(item_id):
    print('liked')
    id = session['user']
    cat_id = db.select(f"select cat_id from items where id={item_id}")
    print(cat_id['cat_id'])
    like_id = db.select(f"select id from likes where user_id = '{id}' and item_id = '{item_id}'")
    if like_id:
        db.insert(f"delete from likes where user_id = '{id}' and item_id = '{item_id}'")
    else:
        db.insert(f"insert into likes (user_id, item_id, liked) values ('{id}', '{item_id}', 'true')")
    return redirect(url_for('user_liked'))


@app.route('/basklike/<int:item_id>')
def bask_like(item_id):
    print('bask')

    id = session['user']
    cat_id = db.select(f"select cat_id from items where id={item_id}")
    print(cat_id['cat_id'])
    like_id = db.select(f"select id from basket where user_id = '{id}' and item_id = '{item_id}'")
    if like_id:
        db.insert(f"delete from basket where user_id = '{id}' and item_id = '{item_id}'")
    else:
        db.insert(f"insert into basket (user_id, item_id) values ('{id}', '{item_id}')")
    return redirect(url_for('user_liked'))

@app.route('/likebask/<int:item_id>')
def like_bask(item_id):
    print('liked')
    id = session['user']
    cat_id = db.select(f"select cat_id from items where id={item_id}")
    print(cat_id['cat_id'])
    like_id = db.select(f"select id from likes where user_id = '{id}' and item_id = '{item_id}'")
    if like_id:
        db.insert(f"delete from likes where user_id = '{id}' and item_id = '{item_id}'")
    else:
        db.insert(f"insert into likes (user_id, item_id, liked) values ('{id}', '{item_id}', 'true')")
    return redirect(url_for('user_basket'))


@app.route('/baskbask/<int:item_id>')
def bask_bask(item_id):
    print('bask')

    id = session['user']
    cat_id = db.select(f"select cat_id from items where id={item_id}")
    print(cat_id['cat_id'])
    like_id = db.select(f"select id from basket where user_id = '{id}' and item_id = '{item_id}'")
    if like_id:
        db.insert(f"delete from basket where user_id = '{id}' and item_id = '{item_id}'")
    else:
        db.insert(f"insert into basket (user_id, item_id) values ('{id}', '{item_id}')")
    return redirect(url_for('user_basket'))

@app.route('/bask/<int:item_id>')
def bask(item_id):
    print('bask')
    if 'user' in session:
        id = session['user']
        cat_id = db.select(f"select cat_id from items where id={item_id}")
        print(cat_id['cat_id'])
        like_id = db.select(f"select id from basket where user_id = '{id}' and item_id = '{item_id}'")
        if like_id:
            db.insert(f"delete from basket where user_id = '{id}' and item_id = '{item_id}'")
        else:
            db.insert(f"insert into basket (user_id, item_id) values ('{id}', '{item_id}')")
        return redirect(url_for('category', cat_id=cat_id['cat_id']))
    else:
        #  add new html with message that people must be authorized
        return redirect(url_for('auth_get'))


@app.route('/category/<int:cat_id>')
def category(cat_id):
    # cat = request.args.get("cat_id")
    if 'user' in session:
        id = session['user']
        print(id)
        ids = db.select(f"select item_id from likes where user_id = '{id}'")
        print(ids)
        ids_list = []
        if len(ids) >= 2:
            for i in ids:
                ids_list.append(i['item_id'])
        elif len(ids) == 1:
            ids_list.append(ids['item_id'])
        print(ids_list)
        items = db.select(f"select * from items where cat_id = '{cat_id}'")

        basks = db.select(f"select item_id from basket where user_id = '{id}'")
        print(basks)
        bask_list = []
        if len(basks) >= 2:
            for i in basks:
                bask_list.append(i['item_id'])
        elif len(basks) == 1:
            bask_list.append(basks['item_id'])
        print(bask_list)

        cat_name = db.select(f"select cat_name from category where id = '{cat_id}'")
        desc = db.select(f"select description from category where id = '{cat_id}'")
        context = {
            'title': cat_name,
            'items': items,
            'desc': desc,
            'ids': ids_list,
            'bask': bask_list
        }
        return render_template('category.html', **context)
    else:
        items = db.select(f"select * from items where cat_id = '{cat_id}'")
        cat_name = db.select(f"select cat_name from category where id = '{cat_id}'")
        desc = db.select(f"select description from category where id = '{cat_id}'")
        context = {
            'title': cat_name,
            'items': items,
            'desc': desc,
        }
        return render_template('cat_without_user.html', **context)


@app.route("/reg", methods=["get"])
def reg_get():  # put application's code here
    return render_template("registration.html")


@app.route("/liked", methods=["get"])
def user_liked():
    id = session['user']
    ids = db.select(f"select item_id from likes where user_id = '{id}'")
    ids_list = set()
    if len(ids) >= 2:
        for i in ids:
            ids_list.add(i['item_id'])
    elif len(ids) == 1:
        ids_list.add(ids['item_id'])
    ids_l = tuple(ids_list)
    items =[]
    if len(ids_l) > 1:
        items = db.select(f"select * from items where id in {ids_l}")
    elif len(ids_l)==1:
        print('aaaaaaaa')
        print(ids_l)
        print(ids_l[0])
        items = db.select(f"select * from items where id = {ids_l[0]}")
        items = [items]
    basks = db.select(f"select item_id from basket where user_id = '{id}'")


    bask_list = []
    if len(basks) >= 2:
        for i in basks:
            bask_list.append(i['item_id'])
    elif len(basks) == 1:
        bask_list.append(basks['item_id'])
    print('bask list')
    print(bask_list)
    print(basks)
    context = {
        'title': {"cat_name": 'Liked items'},
        'items': items,
        'desc': 'your liked list',
        'ids': ids_list,
        'bask': bask_list
    }
    return render_template('liked.html', **context)


@app.route("/basket", methods=["get"])
def user_basket():
    id = session['user']
    ids = db.select(f"select item_id from basket where user_id = '{id}'")
    ids_list = set()
    if len(ids) >= 2:
        for i in ids:
            ids_list.add(i['item_id'])
    elif len(ids) == 1:
        ids_list.add(ids['item_id'])
    ids_l = tuple(ids_list)
    ids2 = db.select(f"select item_id from likes where user_id = '{id}'")
    ids_list2 = set()
    if len(ids2) >= 2:
        for i in ids2:
            ids_list2.add(i['item_id'])
    elif len(ids2) == 1:
        ids_list2.add(ids2['item_id'])
    items = []
    if len(ids_l) > 1:
        items = db.select(f"select * from items where id in {ids_l}")
    elif len(ids_l) == 1:
        items = db.select(f"select * from items where id = {ids_l[0]}")
        items = [items]
    basks = db.select(f"select item_id from basket where user_id = '{id}'")

    bask_list = []
    if len(basks) >= 2:
        for i in basks:
            bask_list.append(i['item_id'])
    elif len(basks) == 1:
        bask_list.append(basks['item_id'])
    print("BASKET")
    print(bask_list)
    total = 0
    for i in items:
        total += int(i['price'])
    context = {
        'title': {"cat_name": 'Your Basket'},
        'items': items,
        'desc': 'your can but this items',
        'ids': ids_list2,
        'bask': bask_list,
        'total': total
    }
    return render_template('basket.html', **context)

@app.template_filter()
def caps(text):
    return text.upper()


@app.route("/reg", methods=["post"])
def reg_post():  # put application's code here
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    bd = request.form.get('bd')
    country = request.form.get('country')
    city = request.form.get('city')
    address = request.form.get('address')
    zipcode = request.form.get('zipcode')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    currency = request.form.get('currency')
    print(currency)
    in_db = db.select(f"select * from users where email = '{email}'")
    print(in_db)
    if not in_db:
        db.insert(f"insert into users (first_name, last_name, "
                  f"birth_date, country, city, address, zipcode,"
                  f" number, email, pass, currency) VALUES ("
                  f"'{fname}', '{lname}', '{bd}', '{country}', '{city}', "
                  f"'{address}', '{zipcode}', '{phone}', '{email}', "
                  f"'{password}', '{currency}')")
    else:
        print("error")
        return render_template("error_reg.html")
    return redirect(url_for('auth_get'))


@app.route('/auth', methods=["GET"])
def auth_get():  # put application's code here
    return render_template("authorization.html")


@app.route('/auth', methods=["POST"])
def auth_post():  # put application's code here
    email = request.form.get("email")
    password = request.form.get("password")
    passw = db.select(f"select pass, id from users where email = '{email}'")
    p = passw['pass']
    id = passw['id']
    if (p == password):
        session['user'] = id
        print('session added')
    else:
        return render_template("error_auth.html")
    return redirect(url_for('main'))


@app.route('/del_session')
def del_session():
    print('session deleted')
    session.pop('user', None)
    return redirect(url_for('main'))


@app.route('/account', methods=['get'])
def account_get():
    id = session['user']
    user = db.select(f"select * from users where id = '{id}'")
    if id == 1:
        return render_template('account_admin.html', user=user)
    return render_template('account.html', user=user)

@app.route('/add', methods=['get'])
def add_get():
    cats = db.select(f"select id, cat_name from category")
    context = {
        'cats': cats
    }
    return render_template('add.html', **context)

@app.route('/add', methods=['post'])
def add_post():
    name = request.form.get('item_name')
    print(name)
    description = request.form.get('description')
    print(description)
    price = request.form.get('price')
    image = request.form.get('image')
    category_id = request.form.get('category_id')
    db.insert(f"insert into items (cat_id, image, item_name, description, price) VALUES ('{category_id}', '{image}', '{name}','{description}', '{price}')")
    id = session['user']
    user = db.select(f"select * from users where id = '{id}'")
    if id == 1:
        return render_template('account_admin.html', user=user)
    return render_template('account.html', user=user)


@app.route('/del', methods=['get'])
def del_get():
    return render_template('del.html')

@app.route('/del', methods=['post'])
def del_post():
    name = request.form.get('item_name')
    db.insert(f"delete from items where item_name = '{name}'")

    id = session['user']
    user = db.select(f"select * from users where id = '{id}'")
    if id == 1:
        return render_template('account_admin.html', user=user)
    return render_template('account.html', user=user)

@app.route('/account', methods=['post'])
def account_post():
    id = session['user']
    user = db.select(f"select * from users where id = '{id}'")

    fname = request.form.get('fname')
    if fname != user['first_name']:
        print('we insert something')
        db.insert(f"update users set first_name = '{fname}' where first_name = '{user['first_name']}' and id = '{id}';")

    lname = request.form.get('lname')
    if lname != user['last_name']:
        print('we insert something')
        db.insert(f"update users set last_name = '{lname}' where last_name = '{user['last_name']}' and id = '{id}';")

    bd = request.form.get('bd')
    if bd != user['birth_date']:
        print('we insert something')
        db.insert(f"update users set birth_date = '{bd}' where birth_date = '{user['birth_date']}' and id = '{id}';")

    country = request.form.get('country')
    if country != user['country']:
        print('we insert something')
        db.insert(f"update users set country = '{country}' where country = '{user['country']}' and id = '{id}';")

    city = request.form.get('city')
    if city != user['city']:
        print('we insert something')
        db.insert(f"update users set city = '{city}' where city = '{user['city']}' and id = '{id}';")

    address = request.form.get('address')
    if address != user['address']:
        print('we insert something')
        db.insert(f"update users set address = '{address}' where address = '{user['address']}' and id = '{id}';")

    zipcode = request.form.get('zipcode')
    if zipcode != user['zipcode']:
        print('we insert something')
        db.insert(f"update users set zipcode = '{zipcode}' where zipcode = '{user['zipcode']}' and id = '{id}';")

    phone = request.form.get('phone')
    if phone != user['number']:
        print('we insert something')
        db.insert(f"update users set first_name = '{phone}' where number = '{user['number']}' and id = '{id}';")

    email = request.form.get('email')
    if email != user['email']:
        print('we insert something')
        db.insert(f"update users set email = '{email}' where email = '{user['email']}' and id = '{id}';")

    password = request.form.get('password')
    if password != user['pass']:
        print('we insert something')
        db.insert(f"update users set pass = '{password}' where pass = '{user['pass']}' and id = '{id}';")

    currency = request.form.get('currency')
    if currency != user['currency']:
        print('we insert something2')
        db.insert(f"update users set currency = '{currency}' where currency = '{user['currency']}' and id = '{id}';")

    return redirect(url_for('account_get'))


if __name__ == '__main__':
    app.run()
