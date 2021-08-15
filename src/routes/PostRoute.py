import logging

from flasgger import swag_from
from flask import Blueprint, request, jsonify

from src.config.Constants import ErrorCode, ErrorMessage
from src.models.PostModel import PostModel
from src.models.UserModel import UserModel
from src.utils.Helper import verify_info_empty

post = Blueprint('post', __name__)


@post.route('/', methods=['POST'])
@verify_info_empty
def create_a_post(local_user: UserModel):
    """API for writing a blog post
       Created by: NHYEN
       Created date: 12/08/2021
            """
    try:
        request_data = request.json
        if 'content' not in request_data or not request_data['content'] or 'title' not in request_data or not \
                request_data[
                    'title']:
            return jsonify(code=ErrorCode.InvalidRequestData, message=ErrorMessage.InvalidRequestData, data=[]), 400
        request_data['user_id'] = local_user.id
        post_model = PostModel(request_data)
        post_model.save()

        return jsonify(code=ErrorCode.Created, message=ErrorMessage.Created, data=[]), 201
    except Exception as e:
        logging.exception(f"Exception create_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@post.route('/', methods=['PUT'])
@verify_info_empty
def update_a_post(local_user: UserModel):
    """
    Update title or content of a post
    Created by: NHYEN
    Created date: 11/08/2021
    :param local_user:
    :return: response message
    """
    try:
        post_id = request.args.get('post_id')
        request_data = request.json
        post_info = PostModel.get_one_blogpost(post_id)
        if not post_info:
            return jsonify(code=ErrorCode.NotFound, message=ErrorMessage.NotFound, data=[]), 404

        post_info.update(request_data)

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@post.route('/', methods=['DELETE'])
@verify_info_empty
def delete_a_post(local_user: UserModel):
    """
        Delete a post by post id
        Created by: NHYEN
        Created date: 11/08/2021
        :param local_user:
        :return: response message
        """
    try:
        post_id = request.args.get('post_id')
        post_info = PostModel.get_one_blogpost(post_id)
        if not post_info:
            return jsonify(code=ErrorCode.NotFound, message=ErrorMessage.NotFound, data=[]), 404
        post_info.delete()

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@post.route('/', methods=['GET'])
@verify_info_empty
def get_posts_a_user(local_user: UserModel):
    """
        Get all post by user id
        Created by: NHYEN
        Created date: 11/08/2021
        :param local_user:
        :return: List of blog posts
        """
    try:
        user_id = request.args.get('user_id')
        list_post = PostModel.get_blogpost_by_user(user_id)

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success,
                       data=[post_inf.serialize for post_inf in list_post]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@post.route('/all', methods=['GET'])
@verify_info_empty
def get_posts_all_users(local_user: UserModel):
    """
        Get all posts of all users
        Created by: NHYEN
        Created date: 11/08/2021
        :param local_user:
        :return: List of blog posts
        """
    try:
        list_post = PostModel.get_all_blogposts()

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success,
                       data=[post_inf.serialize for post_inf in list_post]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500
