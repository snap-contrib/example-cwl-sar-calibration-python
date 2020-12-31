import os
from snapista import Graph, Operator


def get_identifier(safe):

    return os.path.basename(safe).replace(".SAFE", "")


def graph_calibrate_s1(safe):

    identifier = get_identifier(safe)

    g = Graph()

    g.add_node(operator=Operator("Read", formatName="SENTINEL-1", file=f"{safe}"), node_id="read")

    g.add_node(
        operator=Operator("Apply-Orbit-File", continueOnFail="true"),
        node_id="apply-orbit-file",
        source="read",
    )

    g.add_node(
        operator=Operator("Remove-GRD-Border-Noise", borderLimit="2000", trimThreshold="0.2"),
        node_id="noise-removal",
        source="apply-orbit-file",
    )

    g.add_node(
        operator=Operator("Calibration", selectedPolarisations="VV"),
        node_id="calibration",
        source="noise-removal",
    )

    g.add_node(
        operator=Operator("LinearToFromdB", sourceBandNames="Sigma0_VV"),
        node_id="linear",
        source="calibration",
    )

    g.add_node(
        operator=Operator(
            "Terrain-Correction", pixelSpacingInMeter="20.0", demName="SRTM 1Sec HGT"
        ),
        node_id="terrain-correction",
        source="linear",
    )

    g.add_node(
        operator=Operator("Write", file=f"{identifier}_SIGMA0_DB", formatName="GeoTIFF-BigTIFF"),
        node_id="write",
        source="terrain-correction",
    )

    return g
