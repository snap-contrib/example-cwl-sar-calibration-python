$graph:
- baseCommand: sar-calibration
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: sar-calibration:latest
  id: clt
  inputs:
    safe:
      inputBinding:
        position: 1
        prefix: --safe
      type: Directory
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /srv/conda/envs/env_sar_calibration/bin:/srv/conda/envs/env_sar_calibration/snap/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    ResourceRequirement: {}
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: Sentinel-1 GRD calibration
  id: sar-calibration
  inputs:
    safe:
      doc: Path the Sentinel-1 SAFE folder
      label: Path the Sentinel-1 SAFE folder
      type: Directory[]
  label: Sentinel-1 GRD calibration
  outputs:
  - id: wf_outputs
    outputSource:
    - step_1/results
    type:
      items: Directory
      type: array
  requirements:
  - class: ScatterFeatureRequirement
  steps:
    step_1:
      in:
        safe: safe
      out:
      - results
      run: '#clt'
      scatter: safe
      scatterMethod: dotproduct
$namespaces:
  s: https://schema.org/
cwlVersion: v1.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf

