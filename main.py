from aiohttp import web
import json
import os
import os.path
import nextcord as discord
import asyncio
client = discord.Client()
global postl 
postl= 1
while True:
    
    if os.path.isdir(f'posts/{postl}'):
        pass
    else:
        break
    postl += 1
print(postl)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        args = message.content.split(' ')
        arg1 = args[1]
    except:
        pass
    if message.content.startswith('^help'):
        await message.channel.send('lol coming soon')

    if message.content.startswith('^postcount'):
        output = str(len(os.listdir('posts')))
        await message.channel.send(output)

    if message.content.startswith('^postget'):
        try:
            file = open(f'posts/{arg1}/post.post','r')
            info = json.loads(file.read().replace('\n',' '))
            name = info["name"]
            post = info["post"]
            await message.channel.send(f'```{name}\n\n{post}```')
            
        except:
            await message.channel.send('failed - no correct id')
async def run_bot(token):
    await client.start(token)
async def ipcheck(ip):
    banned = open('banned.txt','r')
    output = banned.read().split('\n')
    banned.close()
    for a in output:
        if ip == a:
            return True
        else:
            return False
async def home(request):


    direct = os.listdir('posts')
    file = open('index.html','r')
    posts = '<center><div class=post><p>posted by Bark-it (pinned)</p><p>Welcome to the worst social media ever consisting of the worst security and the second worst user base (first goes to twitter)</p><br></br></div>'
    try:
        page = request.rel_url.query['page']
    except:
        page = 1
    for a in range(3):
        try:

            files = open(f'posts/{a+postl-int(page)*3}/post.post','r')
            output = files.read().replace('\n',' ')
            info = json.loads(output,strict=False)
            name = info["name"]
            post = info["post"].replace('"','\"').replace('<',' &lt').replace('>','&gt;').replace('</textarea>','(nice try)').replace("'",'\'')
            posts = f'{posts} <div class=post><textarea class=name rows="1" readonly>posted by {name}</textarea><textarea readonly class=textpost>{post}</textarea><br><a href=/comments?id={a+postl-int(page)*3}><button>comments(dont wurk)</button></a></br></div> '
        except:
            pass
        
        
    final = file.read().replace('^posts^',posts)
    output = f'{final} </center><div style="position:fixed;left:75%;bottom:0%"><a href=/?page={int(page)-1}><button>last page</button></a><a href=/?page={int(page)+1}><button>next page</button> </a></div>' 
    
    return web.Response(text=output,content_type='text/html')
    

async def post(request):

    print(request.remote)
    bancheck = await ipcheck(request.remote)
    if bancheck == True:
        return web.Response(text='lol you are banned from posting')
    
    global postl
    try:
        name = request.rel_url.query['name'].replace('"','\"').replace('<',' &lt').replace('>','&gt;').replace('</textarea>','(nice try)').replace("'",'\'')
        post = request.rel_url.query['post'].replace('"','\"').replace('<',' &lt').replace('>','&gt;').replace('</textarea>','(nice try)').replace("'",'\'')
        #file = open(str(f'posts/{postl-1}/post.post'),'r')
        #info = json.loads(file.read(),strict=False)
        #post2 = info["post"]
        #if post2 in post:
        #    return web.Response(text='lol you cant dupe posts like that you nerd')
        #file.close()

        if name =='' or post =='' or name.startswith(' ') or name.startswith(' '):
            return web.Response(text='lol you cant send posts like that you nerd')
        postl += 1
        os.makedirs(f'posts/{postl-1}')
        file = open(f'posts/{postl-1}/post.post', "w")
        
        file.write('{\n"name":"'+name+'","post":"'+post+'"\n}')
        file.close()
        channel = client.get_channel(933015976545513473)
        await channel.send(f'```posted by {name}\n\n{post}```')
        return web.Response(text='<meta http-equiv="Refresh" content="0; url=/" />',content_type='text/html')
    except:
        file = open('index.html','r')
        output = file.read().replace('^posts^','<div class=post><form action="/post"><label for="id">post: </label><input type="text" id="name" name="name"><br> <textarea id="post" name="post" rows="4" cols="50"></textarea><br><input type="submit" value="Submit"></form></div>')
        return web.Response(text=output,content_type='text/html')

#async def postcomment(request):


async def tut(request):
    file = open('index.html','r')
    output = file.read().replace('^posts^','<center><h1>just press post and enter stuff</h1>\n<p>I made this because twitter sucks also birds suck dogs better so bark-it ftw</p>\n<h1>api</h1>\n<code>/api?action=postget&id="id"</code><p>This is for getting the posts json contents</p><code>/api?action=postcount</code><p>getting the amount of posts made to bark (-1 to make client making easier and yes please someone make a bark client pls)/p> </center>')
    return web.Response(text=output,content_type='text/html')

async def comments(request):
    try:
        post = request.rel_url.query['id']
    except KeyError:
        return web.Response(text='no id',content_type='text/html')
    try:
        direct = os.listdir(f'posts/{post}/comments')
    except:
        return web.Response(text='this is a old post before comments were a thing, sorry',content_type='text/html')
    index = open('index.html','r')
    output = f'<h1>Comments for post {post}</h1> {index.read()}'
    result = ''
    for a in direct:
        file = open(f'posts/{post}/comments/{a}','r')
        result = f'{result}\n<center><div class=comment><p>{file.read()}</p></div></center>'
        file.close()
    return web.Response(text=output.replace('^posts^',result),content_type='text/html')

async def api(request):
    try:
        action = request.rel_url.query['action']

    except:
        return web.Response(text='none')

    if action =='postget':
        try:
            id = request.rel_url.query['id']
            file = open(f'posts/{id}/post.post','r')
            return web.Response(text=file.read())
        except:
            return web.Response(text='no correct id')
        
                
                #change it later pls k thx

            return web.Response(text=posts)
    if action =='postcount':\
        return web.Response(text=str(len(os.listdir('posts'))-1))



loop = asyncio.get_event_loop()
loop.create_task(run_bot("TOKEN"))
app = web.Application()
app.add_routes([web.get('/', home),
                web.get('/index', home),
                web.get('/post', post),
                web.get('/tutorial', tut),
                web.get('/comments', comments),
                web.get('/api', api),
                web.static('/images', "images", show_index=True)
                
                ])
ws = web.WebSocketResponse()

web.run_app(app)
