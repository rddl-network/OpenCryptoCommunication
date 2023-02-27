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
    This is an UI to directly call crypto primitives on a hardware wallet.
    In this specific case the crypto libraries of Satoshi Lab's Trezor and
    of Blockstream's Jade wallets. The interface is calling directly into 
    the C-code of both code libraries without the use of any API.

    The libraries run on dedicated hardware inside of protected memory
    partitions.

    The technology used in this case is based on an extension to the 
    Open Sound Control ( OSC ) protocol. OSC is meant to be a realtime,
    namespace interface for interconnecting musical devices over any kind 
    of network. The communication happen via SLIP - serial line internet
    protocol


    """
    i = Image(src="https://rddl.io/_next/image?url=https%3A%2F%2Fsuper-static-assets.s3.amazonaws.com%2F64fd875b-2862-4f7a-a3c4-06d5a78e8506%2Fimages%2Fadcbc96c-3a2d-400c-8e8b-65befa507328.png&w=640&q=80", 
                width=300, 
                height=300, 
                fit='contain')

    images = Row(expand=1, wrap=False, scroll="always")

    page.add(i, images)
    page.update()

    nav = Tabs(
            selected_index=0,
            #on_change=tabs_changed,
            tabs=[Tab(text="attest"), Tab(text="seed"), Tab(text="base58 pubkey")],)

    page.add(nav)

    page.add(Text(intro_txt))

    def attest_asset_clicked(e):
        attest_req = ['python3.10', 
                      '/home/nestor/libwally-core/src/test/live_issue2liquid_testnet.py', 
                      str(new_name.value), 
                      str(new_ticker.value), 
                      str(new_domain.value), 
                      str(new_amount.value), 
                      str(new_reissue_amount.value),
                      str(new_precision.value)
        ]

        # For registering the asset within Blockstream's asset registry
        attest_resp = subprocess.run(attest_req, capture_output=True)

        if (attest_resp.returncode == 0):
            print ( attest_resp.stdout.decode ( 'ASCII'))
        else:
            print ( attest_resp.returncode)

        return ( attest_resp.stdout.decode ( 'ASCII'))




    new_name = TextField(hint_text="Define the name of the token", width=300)
    new_ticker = TextField(hint_text="Define the ticker symbol of the token", width=300)
    new_domain = TextField(hint_text="Define issuer domain of token", width=300)

    new_amount = TextField(hint_text="Define amount of token to issue", width=300)
    new_reissue_amount = TextField(hint_text="Define amount of token to re-issue", width=300)
    new_precision = TextField(hint_text="Define precision of token", width=300)

    page.add(Row([Text("Name"), new_name]))
    page.add(Row([Text("Ticker"), new_ticker]))
    page.add(Row([Text("Domain"), new_domain]))

    page.add(Row([Text("Amount"), new_amount]))
    page.add(Row([Text("Reissue"), new_reissue_amount]))
    page.add(Row([Text("Precision"), new_precision]))

    new_task = TextField(hint_text="Whats needs to be done?", width=300)
    btn = ElevatedButton("Attest asset", on_click=attest_asset_clicked)

    page.add(Row([Text("Computation"), btn]))

flet.app(target=main)