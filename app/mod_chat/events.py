from flask import session
from flask_socketio import emit

from app.appModel.models import User
from .. import socketio


@socketio.on('textMessage', namespace='/chat')
def textMessageSent(message):
	"""Mensaje de texto enviado por el cliente a un usuario en particular
		Se envia un evento tanto al emisor como al destinatario
		(emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
	"""

	name = User.query.filter(User.id == session['user_id']).first().name
	emit('updateUiWithTextMessage', {'msg': session.get('name') + ':' + message['msg']}, room=adresseeUserId)
	emit('updateUiWithTextMessage', {'msg': session.get('name') + ':' + message['msg']}, room=session.get('user_id'))




