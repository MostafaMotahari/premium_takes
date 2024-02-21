from pyrogram import Client

accounts_count = input("Enter the number of accounts:")
sessions_export = input("Enter the name of file that sessions strings export to:")

for i in range(int(accounts_count) + 1):
    with Client("Session", api_id=111111, api_hash="Enter Your Api Hash Here ...", in_memory=True) as client:
        session_string = client.export_session_string()
        with open(sessions_export, 'a') as session_file:
            session_file.write(session_string + '\n')
