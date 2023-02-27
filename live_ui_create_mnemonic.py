import subprocess
import sys

import flet
from flet import Checkbox, ElevatedButton, Row, TextField, Text, Image, Tabs, Tab


def main(page):
    page.title = "RDDL attest NFT token to Liquid testnet"
    page.theme_mode = "dark"
    page.padding = 50
    # page.scroll = 'auto'
    page.window_width = 600
    page.window_height = 1000
    page.window_opacity = 1.00
    page.update()

    intro_txt = """
    This is an UI to register the token asset ID and 
    contract metadata directly to the Liquid testnet. 
    Once this is registrationis done the token and all 
    its transactios will be listed with the official
    token name and not just a simple hash.
    """

    nav = Tabs(
            selected_index=0,
            #on_change=tabs_changed,
            tabs=[Tab(text="create menmonic")],)

    page.add(nav)

    page.add(Text(intro_txt))

    def create_mnemonic_clicked(e):
        attest_req = ['python3.10', 
                      '/home/nestor/libwally-core/src/test/live_create_mnemonic.py', 
        ]

        # For listing the asset ID on the server witin the domain of the token issuer
        attest_resp = subprocess.run(attest_req, capture_output=True)

        if (attest_resp.returncode == 0):
            print ( attest_resp.stdout.decode ( 'ASCII'))
        else:
            print ( attest_resp.returncode)

        return ( attest_resp.stdout.decode ( 'ASCII'))
        


    new_task = TextField(hint_text="Whats needs to be done?", width=300)
    btn = ElevatedButton("Create mnemonic", on_click=create_mnemonic_clicked)

    page.add(Row([Text("Computation"), btn]))

flet.app(target=main)