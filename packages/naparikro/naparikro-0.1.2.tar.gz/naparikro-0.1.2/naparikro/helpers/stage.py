from mikro.schema import Representation, RepresentationVariety


class StageHelper:

    def __init__(self, viewer) -> None:
        self.viewer = viewer

    async def open_as_layer(self, rep: Representation):
        rep = await Representation.asyncs.get(id=rep.id)

        if "mask" in rep.tags:
            self.viewer.add_labels(rep.data.sel(c=0).data, name=rep.name, metadata={"rep":rep})
        else:
            array = rep.data.squeeze()
            print(rep.variety)

            if rep.variety == RepresentationVariety.VOXEL or rep.variety == RepresentationVariety.UNKNOWN:
                if "t" in array.dims:
                    raise NotImplementedError("Time series are not supported yet")

                elif "z" in array.dims:
                    if "c" in array.dims:
                        raise NotImplementedError("We have not managed to do things yet...")
                    else:
                        self.viewer.add_image(array.transpose(*list("zxy")), rgb=False, name=rep.name, metadata={"rep":rep}) # why this werid transposing... hate napari
                elif "c" in array.dims:
                    if array.sizes["c"] == 3:
                        self.viewer.add_image(array, rgb=True, name=rep.name, metadata={"rep":rep})
                    else:
                        self.viewer.add_image(array, rgb=False, name=rep.name, metadata={"rep":rep})
                elif "x" in array.dims and "y" in array.dims:
                    self.viewer.add_image(array, rgb=False, name=rep.name, metadata={"rep":rep})
                else:
                    raise NotImplementedError(f"What the fuck??? {array.dims}")


            elif rep.variety == RepresentationVariety.MASK:
                if "t" in array.dims:
                    raise NotImplementedError("Time series are not supported yet")

                if "z" in array.dims:
                    if "c" in array.dims:
                        raise NotImplementedError("We have not managed to do things yet...")
                    else:
                        self.viewer.add_labels(array.transpose(*list("zxy")), name=rep.name, metadata={"rep":rep}) # why this werid transposing... hate napari
            else:
                raise NotImplementedError(f"Cannot open Representation of Variety {rep.variety}")