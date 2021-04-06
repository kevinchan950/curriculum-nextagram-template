from flask import request, render_template, Blueprint, url_for, flash, redirect
from models.donation import Donation
from models.image import Image
from models.user import User
from flask_login import current_user
import braintree
import os

payments_blueprint = Blueprint('payments', __name__, template_folder="templates")

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id= os.getenv("BRAINTREE_ID"),
        public_key= os.getenv("BRAINTREE_PUBLIC_KEY"),
        private_key= os.getenv("BRAINTREE_PRIVATE_KEY")
    )
)

@payments_blueprint.route("/<username>/<imageid>")
def payment_form(username,imageid):
    image = Image.get_by_id(imageid)
    client_token = gateway.client_token.generate()
    return render_template('payments/new.html', client_token=client_token, image=image)

@payments_blueprint.route("/<username>/<imageid>/pay", methods=["POST"])
def accept_payment(username, imageid):
    donation_amount = request.form.get("donation")
    nonce_from_client = request.form["nonce"]
    result = gateway.transaction.sale({
        "amount": donation_amount,
        "payment_method_nonce" : nonce_from_client,
        "options" : {
            "submit_for_settlement" : True
        }
    })
    image = Image.get_by_id(imageid)
    if result:
        donation = Donation(user=current_user.id , image = image, amount = donation_amount)
        donation.save()
        return redirect(url_for('users.show', username=image.user.name))
    else:
        flash("Something went wrong, please try again")   
        return redirect(url_for('payments.payment_form', username=current_user.name, imageid = image.id))