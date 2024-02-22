from pyrogram import Client, filters

api_id = 111111
api_hash = "Fill Here..."
admin_id = "Fill Here ..."
main_group = "Fill Here ..."

app = Client(
    "Handler",
    api_hash=api_hash,
    api_id=api_id
)


@app.on_message(filters.user(admin_id) & filters.chat(main_group) & filters.regex('^ping$'))
async def pong(cli, msg):
    await msg.reply("Pong!")

@app.on_message(filters.user(admin_id) & filters.chat(main_group) & filters.regex('^https://'))
async def join_chats(cli, msg):
    sessions_file = open('sessions_file.txt', 'r')
    counter = 0
    await msg.reply("Please wait ...")
    for session_string in sessions_file.read().split('\n')[:-1]:
        async with Client("Session_open", api_id=api_id, api_hash=api_hash, session_string=session_string.strip(), in_memory=True) as client:
            await client.join_chat(msg.text.split('/')[-1])
            counter += 1
    await msg.reply(f"Joined accounts: [{counter}]")


@app.on_message(filters.user(admin_id) & filters.chat(main_group) & filters.regex('^leave_all$'))
async def leave_all(cli, msg):
    sessions_file = open('sessions_file.txt', 'r')
    counter = 0
    await msg.reply("Please wait ...")
    for session_string in sessions_file.read().split('\n')[:-1]:
        async with Client("Session_open", api_id=api_id, api_hash=api_hash, session_string=session_string.strip(), in_memory=True) as client:
            async for dialog in client.get_dialogs():
                if dialog.chat.username !=main_group:
                    await client.leave_chat(dialog.chat.id)
            counter += 1
    await msg.reply(f"Joined accounts: [{counter}]")


@app.on_message(filters.user(admin_id) & filters.chat(main_group) & filters.regex('^check_winning$'))
async def check_winning(cli, msg):
    sessions_file = open('sessions_file.txt', 'r')
    for session_string in sessions_file.read().split('\n')[:-1]:
        async with Client("Session_open", api_id=api_id, api_hash=api_hash, session_string=session_string.strip(), in_memory=True) as client:
            async for message in await cli.get_chat_history("+42777", limit=1):
                if message:
                    async for self_message in await cli.get_chat_history("me", limit=1):
                        if self_message:
                            if message.id == int(self_message.text):
                                await client.send_message(main_group, 'Ah crap! no any giveaway :(')
                                continue
                            await client.send_message(main_group, f'🎉 Wow! Probably i won a giveaway check me out now! {total_msgs}')
                        else:
                            await cli.send_message("me", f"{message.id}")
                            continue
                else:
                    await client.send_message(main_group, 'Ah crap! no any giveaway :(')

app.run()
