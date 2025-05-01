from Text import cloudflare_text_generator
import spotify_manager
import json
import discord




bot = discord.Client(intents = discord.Intents.all())


@bot.event
async def on_ready():
    channel = await bot.fetch_channel(1315321705853485106)
    await channel.purge()
    await channel.send("SpotiBot Online!")



@bot.event
async def on_message(message: discord.message.Message):

    if not message.author.bot:

        prompt = message.content

        
        response = cloudflare_text_generator.get_response(prompt = prompt, instructions = ["common", "spotify_search"], memory = open('memory.txt', 'r').read())

        try:
            if '`' in response:
                response = response.replace('`', '')

            if response.startswith('json'):
                response = response.replace('json', '')
        except:
            pass

        print(response)
        print(type(response))

        try:
            response = json.loads(response)
        except:
            pass

        if response['operation'] == 'create_playlist':
            spotify_manager.create_playlist(response['playlist_name'])

        elif response['operation'] == 'add_songs_to_playlist':
            playlist_id = spotify_manager.get_playlist_id(response['playlist_name'])

            print(playlist_id)
            print(response['playlist_name'])
            print(response['songs'])

            for song in response['songs']:

                track_uris = spotify_manager.search_tracks(song)
                if track_uris:
                    spotify_manager.add_tracks_to_playlist(playlist_id, track_uris)
                else:
                    pass
                    
        elif response['operation'] == 'delete_playlist':
            playlist_id = spotify_manager.get_playlist_id((response['playlist_name']))
            spotify_manager.delete_playlist(playlist_id)

            
        open('memory.txt', 'a').write(f"User : {message.content}\n")
        open('memory.txt', 'a').write(f"Assistant : {response['confirmation_message']}\n")
        
        await message.channel.send(response['confirmation_message'])



















bot.run("MTM1MjI5NDU4NTk4ODI4ODUzMg.G2Qoey.m0cRoT9dJe3keJ08lhUB0-D6WdD1cHW0ndOPhQ")