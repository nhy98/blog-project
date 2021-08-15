import json
import logging

import requests
from flask import Blueprint, url_for, request, jsonify
from oauthlib.oauth2 import WebApplicationClient
from werkzeug.utils import redirect
from src.config.Constants import Auth, AccountType, ErrorCode, ErrorMessage, UserRole
import os
from src.models.UserModel import UserModel
from src.utils.Helper import verify_access_token

user = Blueprint('user', __name__)
account_type = AccountType.GoogleType


@user.route("/login/<acc_type>")
def login(acc_type):
    """
    Login by google or facebook account
    Created by: NHYEN
    Created date: 11/08/2021
    :param acc_type: facebook / google
    :return: access_token, expires_in
    """
    global account_type
    try:
        # Get google/facebook provider configuration
        account_type = AccountType.GoogleType if acc_type == "google" else AccountType.FacebookType

        app_provider_cfg = __get_app_provider_cfg(account_type)
        authorization_endpoint = app_provider_cfg["authorization_endpoint"]

        # OAuth2 client setup
        client_id = Auth.CLIENT_ID if account_type == AccountType.GoogleType else Auth.FACEBOOK_CLIENT_ID
        client = WebApplicationClient(client_id)

        scope = ["openid", "email", "profile"] if account_type == AccountType.GoogleType else ["email"]
        # Request for google login
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=f"http://localhost:5000/user/callback",
            scope=scope,
        )

        return redirect(request_uri)
    except Exception as e:
        logging.exception(f"Exception login: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@user.route("/callback")
def callback():
    """
    Get access token from authorization code
    Created by: NHYEN
    Created date: 11/08/2021
    :return: access_token, expires_in
    """
    try:
        # Get Google/Facebook authorization code
        code = request.args.get("code")

        # Get google/facebook provider configuration
        app_provider_cfg = __get_app_provider_cfg(account_type)
        token_endpoint = app_provider_cfg[
            "token_endpoint"] if account_type == AccountType.GoogleType else Auth.FACEBOOK_TOKEN_ENDPOINT

        # OAuth2 client setup
        client_id = Auth.CLIENT_ID if account_type == AccountType.GoogleType else Auth.FACEBOOK_CLIENT_ID
        client_secret = Auth.CLIENT_SECRET if account_type == AccountType.GoogleType else Auth.FACEBOOK_SECRET
        client = WebApplicationClient(client_id)

        # Request to get token
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(client_id, client_secret),
        )

        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))

        # Retrieve user information from Google/Facebook
        userinfo_endpoint = app_provider_cfg[
            "userinfo_endpoint"] if account_type == AccountType.GoogleType else Auth.FACEBOOK_USER_ENDPOINT
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.status_code == 200:
            users_email = userinfo_response.json()["email"]
            users_name = userinfo_response.json()["name"]
            fb_user_id = userinfo_response.json()['id'] if account_type == AccountType.FacebookType else None
        else:
            return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500

        # Find user in DB by email
        local_user = UserModel.get_by_email(users_email)
        # Doesn't exist? Add to database
        if not local_user:
            local_user = UserModel(
                {'email': users_email, 'account_type': account_type})
            local_user.name = users_name
            local_user.save()
        else:
            if not local_user.fb_user_id and fb_user_id:
                local_user.update({'fb_user_id': fb_user_id})

        # Return access token and expiration
        response = {
            "access_token": token_response.json()['id_token'] if account_type == AccountType.GoogleType else
            token_response.json()['access_token'],
            "expires_in": token_response.json()['expires_in']
        }
        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[response]), 200
    except Exception as e:
        logging.exception(f"Exception callback: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@user.route("/all", methods=["GET"])
@verify_access_token
def get_all_user(local_user: UserModel):
    """
    Get all users in the system with role administrator
    Created by: NHYEN
    Created date: 11/08/2021
    :param local_user:
    :return: List of users
    """
    try:
        # Check user role
        if local_user.role != UserRole.Admin:
            return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500

        user_info = UserModel.get_all_user()
        data = [us.serialize for us in user_info]
        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=data), 200
    except Exception as e:
        logging.exception(f"Exception get_all_user: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@user.route("/", methods=["GET"])
@verify_access_token
def get_user(local_user: UserModel):
    """
    Get user info by user id
    Created by: NHYEN
    Created date: 11/08/2021
    :param local_user:
    :return: User information
    """
    try:
        user_id = request.args.get('user_id')
        user_info = UserModel.get(user_id)
        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[user_info.serialize]), 200
    except Exception as e:
        logging.exception(f"Exception get_user: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@user.route("/", methods=["PUT"])
@verify_access_token
def update_user(local_user: UserModel):
    """
    Update user information by user id
    Created by: NHYEN
    Created date: 11/08/2021
    :param local_user:
    :return: response message
    """
    try:
        request_data = request.json
        user_info = UserModel.get(local_user.id)
        user_info.update(request_data)

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[]), 200
    except Exception as e:
        logging.exception(f"Exception update_user: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


def __get_app_provider_cfg(account_type):
    return requests.get(Auth.GOOGLE_DISCOVERY_URL).json() if int(
        account_type) == AccountType.GoogleType else requests.get(
        Auth.FACEBOOK_DISCOVERY_URL).json()
