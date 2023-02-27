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
    This is an UI to register the token issuer's domain for a 
    specific asset ID. The listing of the asset ID inside the
    well_known directory on a public accessable sever operated 
    by the issuer is a requirement to successfully register the 
    token and its contract data to the Liquid network.
    """

    nav = Tabs(
            selected_index=0,
            #on_change=tabs_changed,
            tabs=[Tab(text="well-known")],)

    page.add(nav)

    page.add(Text(intro_txt))

    def list_asset_clicked(e):
        attest_req = ['python3.10', 
                      '/home/nestor/libwally-core/src/test/live_well_known.py', 
                      str(new_asset_id.value)
        ]

        # For listing the asset ID on the server witin the domain of the token issuer
        attest_resp = subprocess.run(attest_req, capture_output=True)

        if (attest_resp.returncode == 0):
            print ( attest_resp.stdout.decode ( 'ASCII'))
        else:
            print ( attest_resp.returncode)

        return ( attest_resp.stdout.decode ( 'ASCII'))



    new_asset_id = TextField(hint_text="The asset ID to list", width=300)
    

    page.add(Row([Text("Asset ID"), new_asset_id]))


    new_task = TextField(hint_text="Whats needs to be done?", width=300)
    btn = ElevatedButton("List asset ID", on_click=list_asset_clicked)

    page.add(Row([Text("Computation"), btn]))

flet.app(target=main)