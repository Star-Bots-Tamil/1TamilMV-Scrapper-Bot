from re import match
from urllib.parse import urlparse
from plugins.core.exceptions import DDLException
from plugins.scraper import *
import os
from pyrogram import Client, enums
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID",11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
STRING_SESSION = os.environ.get("STRING_SESSION", "1BVtsOKEBu5Pf_Oesjuxt4TIzNijt1iMjJ8hEa3xtURQFrsd0GFYLhS_XFm2iJ61NfFeKR5icfMSu_SWH3eRvvdZ-X7IyOVFZuQ4sHKoiju_WXCH4uQqqd7vB7_9hGyMbDk7mUgjVKNkRg0trupt-5mu8pAeWAZ3US61kBnLKvsMYSjiaiL3uWI3UDfzyNQzFhf_hXWF_XskD0QrMPS87wEd85iNzXBgBE9Sae2haJ8YppGWxhcGtmJDSqHnDSlxh2dFLBZ1K_o7zxE6i1FrOaqEL_gKW87xqc2W43kCsUj-s9A9GyXdP7aUxu1Mku5j3GyMxEWS79Yku7AfxyeGUYhTw5dXGScE=")
CHAT_ID = int(os.environ.get("CHAT_ID", -1001542301808))

app = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH).start()

def is_excep_link(url):
    return bool(
        match(
            r"https?:\/\/.+\.(1tamilmv|gdtot|filepress|pressbee|gdflix|sharespark)\.\S+|https?:\/\/(sharer|onlystream|hubdrive|katdrive|drivefire|skymovieshd|toonworld4all|kayoanime|cinevood|gdflix|filepress|pressbee|filebee|appdrive)\.\S+",
            url,
        )
    )


async def direct_link_checker(link, onlylink=False):
    domain = urlparse(link).hostname

    # Scraper 
    if bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv(link)
    elif bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv1(link)
    elif bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv2(link)
        
    # Exceptions
    elif bool(match(r"https?:\/\/.+\.technicalatg\.\S+", link)):
        raise DDLException("<b>Bypass Not Allowed !</b>")
    else:
        raise DDLException(
            f"<b>No Bypass Function Found for your Link :</b> <code>{link}</code>"
        )

    if onlylink:
        return blink

    links = []
    while True:
        try:
            links.append(blink)
            blink = await direct_link_checker(blink, onlylink=True)
            if is_excep_link(links[-1]):
                links.append("\n\n" + blink)
                break
  
        except Exception:
            break
    return links

async def process_link_and_send(client, link):
    """
    Processes a link using `tamilmv1` and sends each torrent filename and link to the group/channel.
    """
    try:
        # Get the list of torrent data (filename and links)
        torrent_data = await tamilmv1(link)
        
        for data in torrent_data:
            filename = data.get("filename", "Unknown Filename")  # Extract filename
            torrent_link = data.get("link", "No Link")          # Extract torrent link
            
            # Send the filename and torrent link as a formatted message
            await app.send_message(
                CHAT_ID, 
                f"/qbleech {torrent_link}\n\n<b>Filename :- {filename}</b>",
                parse_mode=enums.ParseMode.HTML
            )
    except Exception as e:
        print(f"Error processing {link}: {e}")  # Log the error for debugging

async def process_link_and_send1(client, link):
    """
    Processes a link using `direct_link_checker2` and sends each magnet link with its filename to the group/channel.
    """
    try:
        # Get the list of magnet data (filename and magnet links)
        magnet_data = await direct_link_checker2(link)
        
        for data in magnet_data:
            filename = data.get("filename", "Unknown Filename")  # Extract filename
            magnet_link = data.get("magnet", "No Magnet Link")   # Extract magnet link
            
            # Send the filename and magnet link as a formatted message
            await app.send_message(
                CHAT_ID, 
                f"/qbleech {magnet_link}\n\n<b>Filename :- {filename}</b>",
                parse_mode=enums.ParseMode.HTML
            )
    except Exception as e:
        print(f"Error processing {link}: {e}")  # Log the error for debugging

async def direct_link_checker1(link):
    """
    Processes a link and extracts torrent links using `tamilmv1`.
    """
    if bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv1(link)
    else:
        raise DDLException(
            f"<b>No Bypass Function Found for your Link:</b> <code>{link}</code>"
        )
async def direct_link_checker2(link):
    """
    Processes a link and extracts magnet links using `tamilmv2`.
    """
    # Check if the link matches a valid 1TamilMV URL pattern
    if bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv2(link)  # Use tamilmv2 to extract magnet links
    else:
        raise DDLException(
            f"<b>No Bypass Function Found for your Link:</b> <code>{link}</code>"
        )
