from flask import Flask, render_template, request, redirect, url_for
import bleach
import re


app = Flask( __name__ )

countries = [
    'Belgium',
    'France',
    'Germany'
]

email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


def is_valid_email( email ):
    return re.match( email_regex, email ) is not None

def sanitize_input( input_str ):
    return bleach.clean( input_str )


@app.route( '/' )
def index():
    return render_template( 'index.html' )

@app.route( '/contact' )
def contact():
    return render_template(
        'contact_form.html',
        countries = countries,
        errors = {}
    )

@app.route( '/submit', methods = [ 'POST' ] )
def submit_form():
    if request.method == 'POST':
        first_name = sanitize_input( request.form[ 'first_name'            ] )
        last_name  = sanitize_input( request.form[ 'last_name'             ] )
        email      = sanitize_input( request.form[ 'email'                 ] )
        country    = sanitize_input( request.form[ 'country'               ] )
        message    = sanitize_input( request.form[ 'message'               ] )
        gender     = sanitize_input( request.form[ 'gender'                ] )
        subject    = sanitize_input( request.form.get( 'subject', 'Others' ) )

        # Honeypot
        if request.form.get( 'website' ):
            return redirect( url_for( 'index' ) )

        errors = {}

        if not first_name:
            errors[ 'first_name' ] = 'First name is required.'
        if not last_name:
            errors[ 'last_name' ]  = 'Last name is required.'
        if not email:
            errors[ 'email' ]      = 'Email is required.'
        elif not is_valid_email( email ):
            errors[ 'email' ]      = 'Invalid email address'
        if not country:
            errors[ 'country' ]    = 'Country is required.'
        if not message:
            errors[ 'message' ]    = 'Message is required.'
        if not gender:
            errors[ 'gender' ]     = 'Gender is required.'

        if errors:
            return render_template(
                'contact_form.html',
                countries  = countries,
                errors     = errors,
                first_name = first_name,
                last_name  = last_name,
                email      = email,
                country    = country,
                message    = message,
                gender     = gender,
                subject    = subject
            )

        return render_template(
            'thank_you.html',
            first_name = first_name,
            last_name  = last_name,
            email      = email,
            country    = country,
            message    = message,
            gender     = gender,
            subject    = subject
        )


if __name__ == '__main__':
    app.run( debug = True )
