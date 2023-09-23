from market import app
from flask import render_template, redirect, url_for, flash, request, session, abort
from market.forms import RegisterForm,  LoginForm, PurchaseItemForm, SellItemForm, WithdrawlForm, RechargeForm, PayoutForm                  
from market.models import Item, User, Payout, Buyer, Recharge, Withdrawlss
from market import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from datetime import date, time, timedelta
import  datetime 
import datetime as dt
from pytz import utc
from random import randint 
import random
import os
import string



@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    register_time = datetime.datetime.now()
    register_time = register_time.replace(second=0, microsecond=0)
    if form.validate_on_submit():
        referral_code=form.referral_code.data
        username=form.username.data
        link_id=generate_referral_code()
     # Check if referral code exists in the database
        referred_by = None 
        if referral_code:
            referred_by_user = User.query.filter_by(referral_code=referral_code).first()
            
        if referred_by_user:
            referred_by = referred_by_user.id 

        # Add referral bonus to referred user's account
        if referred_by:
            # referred_by_user.referred_bonus += 100
            db.session.commit()

    

        user_to_create = User(username=form.username.data, password=form.password1.data, with_password=form.with_password.data, refer_code=link_id, referral_code=generate_referral_code(), referred_by=referred_by, register_time=register_time)
        db.session.add(user_to_create)    
        db.session.commit()
        flash('Register successful')
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category='danger')
    return render_template('index.html', form=form)

@app.route('/market', methods=['GET', 'POST'])
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method =="POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.owner = current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()
                create = Buyer(item_owner=current_user.id, item_name=p_item_object.name)
                db.session.add(create)
                db.session.commit()
                flash("Purchase successful !", category='danger')
            else:
                flash("You don't have enough money ! Please recharge")    

        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(price=499).all()
        toms = Item.query.filter_by(cycle=3).all()
        return render_template('market.html', items=items, purchase_form=purchase_form, toms=toms)              


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()   
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Login successful')
            return redirect(url_for('market_page'))
            
        else:
            flash('Not match!', category='danger')    
    return render_template('login.html', form=form)       

@app.route('/logout')
def logout_page():
    logout_user()
    flash('logout successful')
    return redirect(url_for("login_page"))

@app.route('/withdrawl', methods=['GET', 'POST'])
def withdrawl_page():  
    # withdraw_time = datetime.datetime.now()
    # withdraw_time = withdraw_time.replace(second=0, microsecond=0)
    # attempted_withdraw = Payout.query.filter_by(check=current_user.id).first()
    # attempted_withdrawl = Payout.query.filter_by(check=current_user.id).order_by(Payout.ac_number.desc()).first()
    # form = WithdrawlForm(obj=attempted_withdrawl) if attempted_withdrawl else WithdrawlForm()
    # enter_amount = form.withdraw.data
    # withdraw23 = enter_amount*0.90
    # if form.validate_on_submit():
    #     if attempted_withdraw:
    #         flash('Bank account already bind')
    #     else:
    #         if enter_amount>=130 and current_user.budget>=enter_amount:
    #             current_user.budget -= enter_amount
    #             ac = Payout(h_name=form.h_name.data,ac_name=form.ac_name.data, ac_number=form.ac_number.data, ac_ifsc=form.ac_ifsc.data,withdraw=form.withdraw.data, withdraw2=withdraw23, check=current_user.id, withdraw_time=withdraw_time)
    #             db.session.add(ac)
    #             db.session.commit()
    #             acc = Payout
    #             flash('Withdraw submitted !')
    #         else:
    #             flash('withdraw amount is below 130 or insufficient balance !', category='danger')
    # return render_template('withdrawl.html', form=form)

    form=WithdrawlForm()
    if form.validate_on_submit():
           
           ac = Payout(h_name=form.h_name.data, p_name=form.p_name.data, ac_name=form.ac_name.data, ac_number=form.ac_number.data, ac_ifsc=form.ac_ifsc.data, w_pass=form.w_pass.data,  checkk=current_user.id)
           db.session.add(ac)
           db.session.commit()
           acc = Payout
           flash('Bank added successful')
           return redirect(url_for('withdrawls'))       
    if form.errors != {}:
       for err_msg in form.errors.values():
          flash(f'There was an error: {err_msg}', category='danger')       
    return render_template('withdrawl.html', form=form)    
    





@app.route('/Income')
def income_page():
    buy = Buyer.query.filter_by(item_owner=current_user.id).first()
    return render_template('income.html')

@app.route('/icon')
def icon_page():
    return render_template('icon.html')

@app.route('/my')
def my():
    cars = User.query.filter_by(referred_by=current_user.id).all()
    total_referincome2 = sum(car.referred_bonus for car in cars)
    return render_template('my.html', cars=cars, total_referincome2=total_referincome2)

@app.route('/referrals/<referral_code>')
@login_required
def referrals(referral_code):
    referral_link = request.host_url + 'register?referral_code=' + referral_code
    return render_template('referrals.html', referral_link=referral_link)

def generate_referral_code():
    letters = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choice(letters + digits) for i in range(6))

@app.route('/team')
def team():
    friends = User.query.filter_by(referred_by=current_user.id).all()
    total_referincome = sum(friend.recharge_amount for friend in friends)
    tits = User.query.filter_by(referred_by=current_user.id).all()
    total = sum(tits.total for tit in tits)
    # toys = User.query.filter_by(referred_by=current_user.id).all()
    # total_referincome1 = sum(toy for toy in toys)
    print("Total Budget:", total_referincome)
    # total_profit = (profit.recharge_amount for profit in profits)
    # total = sum(profit.recharge_amount)
    return render_template('team.html', friends=friends, tits=tits,  total_referincome=total_referincome, total=total)

@app.route('/team1')
def team1():
    pets = User.query.filter_by(referred_by=current_user.id).all()
    
    user = current_user
    bonus = user.recharge_amount*0.2
    user.referred_bonus += bonus
    user.update_referred_bonus()
    return render_template('team1.html', pets=pets)
    
@app.route('/my product')
def record():
    return render_template('record.html')

@app.route('/account record')
def account():
    children = Payout.query.filter_by(checkk=current_user.id).all()
    return render_template('account.html', children=children)

@app.route('/personal info')
def personal():
    records = Recharge.query.filter_by(rech_owner=current_user.id).all()
    return render_template('info.html', records=records)

@app.route('/company')
def company():
    boys = Buyer.query.filter_by(item_owner=current_user.id).all()
    return render_template('company.html', boys=boys)

@app.route('/withdrawls', methods=['GET', 'POST'])
def withdrawls():
    form=PayoutForm()
    attempted_withdraw = Withdrawlss.query.filter_by(user_id=current_user.id).first()
    bank = Payout.query.filter_by(checkk=current_user.id).first()
    amt = form.amount.data
    withdraw_time = datetime.datetime.now()
    withdraw_time = withdraw_time.replace(second=0, microsecond=0)
    # h=0.90
    # withdraw23 = amt*h
 
    if not bank:
        flash('Please bind bank first')
        return redirect(url_for('withdrawl_page'))

    if form.validate_on_submit():
        amt = form.amount.data
        if attempted_withdraw:
            flash('Per day 1 withdrawl is allowed')
            # if not bank:               
            #     flash('Bind account not bind')
            # return redirect(url_for('withdrawl_page'))
        else:
           if (amt >= 149 and current_user.budget >= amt):
               current_user.budget -= amt         
               pay = Withdrawlss(amount=form.amount.data, passs=form.passs.data, user_id=current_user.id, withdraw2=form.amount.data*0.90, withdraw_time=withdraw_time)
               db.session.add(pay)
               db.session.commit()
               flash('Withdrawl submitted')
           else:
               flash('Minimum withdrawl amount is 150')
    # children = Payout.query.filter_by(check=current_user.id).all()
    return render_template('with.html', form=form, bank=bank )


 



@app.route('/method1', methods=['GET', 'POST'])
def method1():
    form = RechargeForm()
    amount_rech = form.rech_amount.data
    if form.validate_on_submit():
        if amount_rech>=499:
            rech = Recharge(rech_amount=form.rech_amount.data, utr=form.utr.data, rech_owner=current_user.id)
            db.session.add(rech)
            db.session.commit()
            flash('Submit successful!')
        else:
            flash('Minimum recharge amount is 499', category='danger')
    return render_template('method1.html', form=form)


@app.route('/method2', methods=['GET', 'POST'])
def method2():
    form = RechargeForm()
    amount_rech = form.rech_amount.data
    if form.validate_on_submit():
        if amount_rech>=499:
            rech = Recharge(rech_amount=form.rech_amount.data, utr=form.utr.data, rech_owner=current_user.id)
            db.session.add(rech)
            db.session.commit()
            flash('Submit successfully!')
        else:
            flash('Minimum recharge amount is 499', category='danger')
    return render_template('method2.html', form=form)

@app.route('/method3', methods=['GET', 'POST'])
def method3():
    form = RechargeForm()
    amount_rech = form.rech_amount.data
    if form.validate_on_submit():
        
        if amount_rech>=499:
            rech = Recharge(rech_amount=form.rech_amount.data, utr=form.utr.data, rech_owner=current_user.id)
            db.session.add(rech)
            db.session.commit()
            flash('Submit successfully!')
        else:
            flash('Minimum recharge amount is 499', category='danger')
    return render_template('method3.html', form=form)

@app.route('/recharge')
def recharge():
    return render_template('recharge.html')




@app.route('/withdrawl paasword')
def withpass():
    return render_template('withpass.html')

@app.route('/login password')
def loginpass():
    return render_template('loginpass.html')

@app.route('/personal setting')
def setting():
    return render_template('setting.html')



@app.route('/all types')
def all_types():
    cats = Recharge.query.filter_by(utr=current_user.id).all()
    bats = Withdrawlss.query.filter_by(user_id=current_user.id).all()
    return render_template('alltypes.html', cats=cats, bats=bats)



@app.route('/recharges')
def recharges():
    rats = Recharge.query.filter_by(utr=current_user.id).all()
    return render_template('recharges.html', rats=rats)


@app.route('/withs')
def withs():
    bikes = Withdrawlss.query.filter_by(user_id=current_user.id).all()
    # total_referincome = sum(friend.recharge_amount for friend in friends)
    return render_template('withs.html', bikes=bikes)
