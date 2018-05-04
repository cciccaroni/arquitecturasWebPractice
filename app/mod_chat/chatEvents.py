from flask import session, url_for
from flask_socketio import join_room, emit
import wave
import uuid
from app import socketio, app
from app.appModel.models import User
from app.mod_conversation.conversation_api import conversation_manager


@socketio.on('joined', namespace='/chat')
def joined():
    # """Sent by clients when they enter a room.
    # A status message is broadcast to all people in the room."""
    user_id = session.get('user_id', None)
    
    # Join into my room
    join_room(user_id)

    # Broadcast of my new status to all users.
    # status = {'msg': {'id': my_user.id, 'name': str(my_user.name), 'status': 'ENTERED'}}
    # users = User.query.all()
    # for user in users:
    #     emit('status', status, room=user.id)



# Se deberia iterar el toIds, que vienen todos los ids a los que hay que enviar el evento
@socketio.on('textMessage', namespace='/chat')
def textMessage(json):
    """Mensaje de texto enviado por el cliente a un usuario en particular
      Se envia un evento tanto al emisor como al destinatario
      (emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
    """
    user_id = session.get('user_id', None)
    if not user_id:
        return

    my_user = User.query.get(user_id)
    if not my_user:
        return

    #TODO: armar un chat_manager que tenga el conversation_manager adentro
    conversation_manager.log_message(user_id,json['msg'],json['conversationId'])

    status = {'msg': json['msg'], 'from': json['fromName']}
    # TODO: SACAR ESTE EVAL POR EL AMOR DE DIOS!
    for recipient in eval(json['toIds']):
        emit('uiTextMessage', status, room=recipient)
    print("mensaje enviado a los miembros del chat")

@socketio.on('start-recording', namespace='/chat')
def start_recording(options):
    """Start recording audio from the client."""
    id = uuid.uuid4().hex  # server-side filename
    session['wavename'] = id + '.wav'
    wf = wave.open(app.config['FILEDIR'] + session['wavename'], 'wb')
    wf.setnchannels(options.get('numChannels', 1))
    wf.setsampwidth(options.get('bps', 16) // 8)
    wf.setframerate(options.get('fps', 44100))
    session['wavefile'] = wf


@socketio.on('write-audio', namespace='/chat')
def write_audio(data):
    """Write a chunk of audio from the client."""
    session['wavefile'].writeframes(data)


@socketio.on('end-recording', namespace='/chat')
def end_recording(recipients, conversationId, loggedUserName):
    """Stop recording audio from the client."""
    status = {'url': url_for('static', filename='_files/' + session['wavename']), 'from': loggedUserName}
    for recipient in recipients:
        emit('add-wavefile', status, room=recipient)
    session['wavefile'].close()
    del session['wavefile']
    del session['wavename']





#dejo comentado hasta que lo metamos posta
# @socketio.on('imageMessage', namespace='/chat')
# def imageMessage(message, users):
#     """Imagen enviado por el cliente a un usuario en particular
#       Se envia un evento tanto al emisor como al destinatario
#       (emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
#     """
#     user_id = session.get('user_id', None)
#     if not user_id:
#       return
#
#     my_user = User.query.get(user_id)
#     if not my_user:
#       return
#
#     status = {'msg': message, 'from': {'name': str(my_user.name), 'id': my_user.id}}
#     for user in users:
#         emit('image', status, room=int(user))
