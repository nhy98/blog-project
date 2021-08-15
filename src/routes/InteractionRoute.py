import logging

from flask import Blueprint, request, jsonify

from src.config.Constants import ErrorCode, ErrorMessage
from src.models.InteractionModel import InteractionModel
from src.models.PostModel import PostModel
from src.models.UserModel import UserModel
from src.utils.Helper import verify_access_token

interaction = Blueprint('interaction', __name__)


@interaction.route('/', methods=['GET'])
@verify_access_token
def get_interaction_by_post(local_user: UserModel):
    """
        Get interaction of a post by post id
        Created by: NHYEN
        Created date: 11/08/2021
        :param local_user:
        :return: List of interaction
    """
    try:
        post_id = request.args.get("post_id")
        inters_response = InteractionModel.get_interaction_by_user_and_post(post_id)

        list_inter_info, list_name, list_email = [], [], []
        for inter in inters_response:
            list_inter_info.append(inter['InteractionModel'])
            list_name.append(inter['name'])
            list_email.append(inter['email'])

        list_interinfo_response = [inter.serialize for inter in list_inter_info]

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success,
                       data=[
                           {"interaction": list_interinfo_response, "user_name": list_name,
                            "user_email": list_email}]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@interaction.route('/', methods=['POST'])
@verify_access_token
def create_an_interaction(local_user: UserModel):
    """
        Make an interaction for a post
        Created by: NHYEN
        Created date: 11/08/2021
        :param local_user:
        :return: response message
    """
    try:
        request_data = request.json
        if 'post_id' not in request_data or not request_data['post_id']:
            return jsonify(code=ErrorCode.InvalidRequestData, message=ErrorMessage.InvalidRequestData, data=[]), 400

        post_info = PostModel.get_one_blogpost(request_data['post_id'])
        if not post_info:
            return jsonify(code=ErrorCode.NotFound, message=ErrorMessage.NotFound, data=[]), 404

        request_data['user_id'] = local_user.id
        inter_model = InteractionModel(request_data)
        inter_model.save()

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@interaction.route('/', methods=['DELETE'])
@verify_access_token
def delete_an_interaction(local_user: UserModel):
    """
        Delete interaction by interaction id
        Created by: NHYEN
        Created date: 11/08/2021
        :param local_user:
        :return: response message
        """
    try:
        inter_id = request.args.get('inter_id')
        inter_info = InteractionModel.get_one_blogpost(inter_id)
        if not inter_info:
            return jsonify(code=ErrorCode.NotFound, message=ErrorMessage.NotFound, data=[]), 404

        inter_info.soft_delete()

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500


@interaction.route('/post', methods=['DELETE'])
@verify_access_token
def delete_an_interaction_by_post(local_user: UserModel):
    """
        Delete an interaction by post id
        Created by: NHYEN
        Created date: 11/08/2021
        :param local_user:
        :return: response message
        """
    try:
        post_id = request.args.get('post_id')
        inter_info = InteractionModel.get_interaction_by_user_and_post(post_id, local_user.id)
        if not inter_info:
            return jsonify(code=ErrorCode.NotFound, message=ErrorMessage.NotFound, data=[]), 404
        inter_info.soft_delete()

        return jsonify(code=ErrorCode.Success, message=ErrorMessage.Success, data=[]), 200
    except Exception as e:
        logging.exception(f"Exception update_a_post: {e}")
        return jsonify(code=ErrorCode.InternalServerError, message=ErrorMessage.InternalServerError, data=[]), 500

