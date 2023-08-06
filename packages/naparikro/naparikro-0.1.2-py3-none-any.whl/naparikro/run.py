import contextlib

import napari
from mikro.schema import Representation
from naparikro.helpers.stage import StageHelper
from arkitekt.agents import AppAgent
from arkitekt import SearchWidget
import qasync
import numpy as np
import argparse
import asyncio
from rich.console import Console

console = Console()


async def main(viewer, **kwargs):
   
    agent = AppAgent(**kwargs)

    stage_helper = StageHelper(viewer)

    @agent.register(widgets={
        "rep": SearchWidget(query="""
            query Search($search: String){
                options: representations(name: $search) {
                    value: id
                    label: name
                }
            }
        """)
    })
    async def blower(rep: Representation) -> Representation:
        """Show Blower

        Shows the Image on Napari

        Args:
            rep (Representation): [description]

        Returns:
            Representation: [description]
        """
        print("hallo is doing this")
        await stage_helper.open_as_layer(rep)
        
        return rep

    try:
        await agent.aprovide()
    except Exception:
        console.print_exception()



def app_main(**kwargs):
    viewer = napari.Viewer()
    app = napari.qt.get_app()
    loop = qasync.QSelectorEventLoop(app)
    asyncio.set_event_loop(loop)
    loop.create_task(main(viewer, **kwargs))
    napari.run()





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Which config file to use', default="bergen.yaml", type=str)
    args = parser.parse_args()

    app_main(config_path=args.config)
