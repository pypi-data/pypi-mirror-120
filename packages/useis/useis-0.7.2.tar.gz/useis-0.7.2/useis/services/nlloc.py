from uquake.grid import nlloc
from uquake.nlloc import nlloc as nlloc2
from .grid_service_pb2 import VelocityGrid3D as VG3D
from .grid_service_pb2 import Srces as PB2_Srces
from .grid_service_pb2 import Site as PB2_Site
import numpy as np

__default_float_type__ = nlloc.__default_float_type__


class VelocityGrid3D(nlloc.VelocityGrid3D):
    def __init__(self, network_code, data_or_dims, origin, spacing,
                 phase='P', value=0, float_type=__default_float_type__,
                 model_id=None, **kwargs):

        super().__init__(network_code, data_or_dims, origin, spacing,
                         phase=phase, value=value, float_type=float_type,
                         model_id=model_id)
        pass

    @classmethod
    def from_velocity_grid_3d(cls, velocity_grid: nlloc.VelocityGrid3D):
        vg = velocity_grid
        return cls(vg.network_code, vg.data, vg.origin, vg.spacing,
                   phase=vg.phase, float_type=vg.float_type,
                   model_id=vg.model_id)

    @classmethod
    def from_proto(cls, proto: VG3D):
        data = np.array(proto.data)
        data = data.reshape(proto.dimensions)
        return cls(proto.network_code, data, proto.origin, proto.spacing,
                   phase=proto.phase, model_id=proto.model_id)

    def to_proto(self):
        vg3d = VG3D()
        vg3d.network_code = self.network_code
        vg3d.origin.extend(self.origin)
        vg3d.spacing.extend(self.spacing)
        vg3d.dimensions.extend(self.dimensions)
        vg3d.data.extend(self.data.ravel().tolist())
        vg3d.phase = self.phase
        vg3d.model_id = self.model_id

        return vg3d


class Srces(nlloc2.Srces):
    def __init__(self,  sites=[], units='METERS'):
        super().__init__(sites=sites, units=units)

    @classmethod
    def from_proto(cls, proto_sites):
        sites = []
        for proto_site in proto_sites:
            site = nlloc2.Site(proto_site.label, proto_site.x, proto_site.y,
                              proto_site.z, proto_site.elev)
            sites.append(site)

        return cls(sites=sites)

    @classmethod
    def from_srces(cls, srces):
        return cls(sites=srces.sites, units=srces.units)

    def to_proto(self):
        proto_sites = []
        for site in self.sites:
            proto_site = PB2_Site()
            proto_site.label = site.label
            proto_site.x = site.x
            proto_site.y = site.y
            proto_site.z = site.z
            proto_site.elev = site.elev
            proto_sites.append(proto_site)

        return proto_sites





