
from random import choice
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from pycricbuzz import Cricbuzz
c = Cricbuzz()
live_matches=[]
live_scores=[]
completed_match_score=[]
matches = c.matches()
ask = ["hi", "hello","hey"]
general=['ok','thank you','thanks']
genaral_ans=['ok','thats great','its ok']
hi = ["hi", "hello", "Hello too","hey how can i help you?"]
error = ["sorry, i don't know", "what u said?",'Can you ask again?','sorry i dont have answer for your question']
#get the all matches which are currently in cricbuzz
for i in matches:

    if i['mchstate'] == 'inprogress': #it checks whether the match is lie or not

         #getting live score list using match id
        live_scores.append(Cricbuzz().livescore('{}'.format(i['id'])))

    elif i['mchstate']=='complete' or 'mom':


        completed_match_score.append(Cricbuzz().livescore('{}'.format(i['id'])))

def get_score(i,client):
    if len(i)>0:

        client.send(bytes(i['batting']['team'] + ' vs ' + i['bowling']['team'] + " \n ","utf8"))
        for j in range(len(i['batting']['score'])):
            client.send(bytes(i['batting']['team'] + ': ' + i['batting']['score'][j]['runs'] + '/' + i['batting']['score'][j]['wickets'] + (" ({over})".format(over=i['batting']['score'][j]['overs'])) + "[INNINGS NUMBER:" + i['batting']['score'][j]['inning_num'] + ']'+'  ',"utf8"))
        for j in range(len(i['bowling']['score'])):
            client.send(bytes((i['bowling']['team'] + ': ' + i['bowling']['score'][0]['runs'] + '/' + i['bowling']['score'][j]['wickets'] + (" ({over})".format(over=i['bowling']['score'][j]['overs'])) + "[INNINGS NUMBER:" +i['bowling']['score'][j]['inning_num'] + ']'),'utf8'))
def live_score_between_teams(i,msg,client):
    if len(i)>0:
        if i['batting']['team'] in msg and i['bowling']['team'] in msg:
            for j in range(len(i['batting']['score'])):
                client.send(bytes(i['batting']['team'] + ': ' + i['batting']['score'][j]['runs'] + '/' + i['batting']['score'][j]['wickets'] + (" ({over})".format(over=i['batting']['score'][j]['overs'])) + "[INNINGS NUMBER:" +i['batting']['score'][j]['inning_num'] + ']','utf8'))
            for j in range(len(i['bowling']['score'])):
                client.send(bytes(i['bowling']['team'] + ': ' + i['bowling']['score'][0]['runs'] + '/' + i['bowling']['score'][j]['wickets'] + (" ({over})".format(over=i['bowling']['score'][j]['overs'])) + "[INNINGS NUMBER:" +i['bowling']['score'][j]['inning_num'] + ']','utf8'))
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cricbot ! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name

    clients[client] = name

    while True:
        msg1 = client.recv(BUFSIZ).decode("utf8")
        msg=msg1.lower()
        if msg != "quit":
            client.send(bytes("BOT : ","utf8"))
            if 'live score' in msg or 'live scores' in msg:
                if len(live_scores)>0:
                    for i in live_scores:
                        get_score(i, client)
                else:
                    client.send(bytes("SORRY,Currently no matches are running","utf8"))



            elif 'completed score' in msg or 'completed scores' in msg:
                if len(completed_match_score)>0:
                    for i in completed_match_score:
                        get_score(i, client)
                else:
                    client.send(bytes("Sorry!! we dont have that data right now"))


            elif 'status' in msg and 'between' in msg:
                for i in matches:
                    if (i['team1']['name']).lower() in msg and (i['team2']['name']).lower() in msg:
                        client.send(bytes(i['status'],'utf8'))


            elif 'score' in msg and 'between' in msg:
                for i in matches:
                    if (i['team1']['name']).lower() in msg and (i['team2']['name']).lower() in msg:
                        if i['mchstate'] == 'abandon' or i['mchstate'] == 'preview':
                            client.send(bytes(i['status'],'utf8'))

                for i in live_scores:
                    live_score_between_teams(i, msg, client)
                for i in completed_match_score:
                    live_score_between_teams(i, msg, client)

            elif 'squad' in msg or 'squads' in msg:
                for i in matches:
                    if (i['team1']['name']).lower() in msg:
                        client.send(bytes(i['team1']['name'] + "  SQUAD : ",'utf8'))
                        for j in i['team1']['squad']:
                            client.send(bytes(j,'utf8'))
                            client.send(bytes(', ','utf8'))
                    client.send(bytes('\n','utf8'))
                    if (i['team2']['name']).lower() in msg:
                        client.send(bytes(i['team2']['name'] + "SQUAD : ",'utf8'))
                        for j in i['team2']['squad']:
                            client.send(bytes(j,'utf8'))
                            client.send(bytes(', ', 'utf8'))
            elif 'match details' in msg or 'details' in msg:
                for i in matches:
                    if (i['team1']['name']).lower() in msg and (i['team2']['name']).lower() in msg:
                        client.send(bytes(" SERIES : " + i['srs'],'utf8'))
                        client.send(bytes(', ', 'utf8'))
                        client.send(bytes("MATCH : " + i['mnum'],'utf8'))
                        client.send(bytes(', ', 'utf8'))
                        client.send(bytes("MATCH TYPE : " + i['type'],'utf8'))
                        client.send(bytes(', ', 'utf8'))
                        client.send(bytes("VENUE : " + i['venue_name'] + "  " + i['venue_location'],'utf8'))
                        client.send(bytes(', ', 'utf8'))
                        client.send(bytes("TOSS : " + i['toss'],'utf8'))
                        client.send(bytes(', ', 'utf8'))
                        client.send(bytes('MAIN UMPIRES : ' + i['official']['umpire1']['name'] + ", " + i['official']['umpire2']['name'],'utf8'))
                        client.send(bytes(', ', 'utf8'))
                        client.send(bytes('3RD UMPIRE : ' + i['official']['umpire3']['name'] + '\n','utf8'))
                        client.send(bytes(', ', 'utf8'))
                        client.send(bytes("DATE AND TIME : " + i['start_time'],'utf8'))

            elif msg in ask:
                client.send(bytes(choice(hi),"utf8"))
            elif msg in general:
                client.send(bytes(choice(genaral_ans),"utf8"))
            else:
                client.send(bytes(choice(error),"utf8"))
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()